from os import environ

from time import sleep

import json

from uuid import uuid4

import requests

from rest_framework import status

from celery import shared_task

from common.response_class import GenericResponse

from agent.models import Agent

from payment.models import Payment
from payment.serializers import PaymentSerializer

from reservation.models import Reservation, Room, Guest

from external_api.logs import save_log
from external_api.tasks.tbo.common import (PAYMENT_TYPE, BOOK_URL, HEADERS, PROVIDER_ID,
    BOOKING_DETAIL_URL, PAYMENT_METHOD
)
from external_api.tasks.tbo.room_detail_prebook import tbo_get_room_prebook_details


TITLE_DICT = {
    'MR': ('Mr', 'Adult'),
    'MS': ('Ms', 'Adult'),
    'CH': ('Mr', 'Child')
}


def tbo_book(data, user):
    room_details = tbo_get_room_prebook_details(data).data
    payment = Payment.objects.create(
        agent=Agent.objects.get(user=user),
        payment_type_id=PAYMENT_TYPE,
        commission=data['payment']['commission'],
        subtotal=room_details['rooms']['price'],
        total=data['payment']['total']
    )
    reservation = Reservation.objects.create(
        payment=payment,
        hotel_id=data['hotel_id'],
        search_parameters=data['filters'],
        booking_code=room_details['rooms']['booking_code'],
        policies=data['policies']
    )
    rooms_list = []
    guests_list = []
    for x in range(len(room_details['rooms']['rooms_details'])):
        room_id = str(uuid4())
        rooms_list.append(
            Room(
                id=room_id,
                reservation=reservation,
                name=room_details['rooms']['rooms_details'][x]['name'],
                price=room_details['rooms']['rooms_details'][x]['price'],
                supplements=room_details['rooms']['rooms_details'][x]['supplements']
            )
        )
        for guest in data['rooms'][x]['guests']:
            guests_list.append(
                Guest(
                    room_id=room_id,
                    traveler_id=guest['traveler_id'],
                    is_lead=guest['is_lead']
                )
            )
    Room.objects.bulk_create(rooms_list)
    Guest.objects.bulk_create(guests_list)
    if data['payment']['link']:
        print('send_email')
    return GenericResponse(
        data=PaymentSerializer(payment).data,
        status_code=status.HTTP_201_CREATED
    )


def get_customer_names(room):
    return [
        {
            'Title': TITLE_DICT[g.traveler.title][0],
            'FirstName': g.traveler.first_name,
            'LastName': g.traveler.last_name,
            'Type': TITLE_DICT[g.traveler.title][1]
        } for g in room.room_guests.all()
    ]


@shared_task
def update_book_status(reservation_id):
    r = Reservation.objects.get(id=str(reservation_id))
    counter = 0
    payload = {
        'ConfirmationNumber': r.confirmation_number,
        'PaymentMode': PAYMENT_METHOD
    }
    while counter < 5:
        response = requests.post(
            BOOKING_DETAIL_URL,
            headers=HEADERS,
            data=json.dumps(payload)
        )
        save_log(PROVIDER_ID, BOOKING_DETAIL_URL, payload, response.status_code, response.json())
        if response.status_code == '200' and response.json()['Status']['Code'] == 200:
            if response.json()['BookingDetail']['BookingStatus'] == 'Confirmed':
                r.reservation_status = '5955f72b-3afd-4137-8a69-dc9d1eb24253' # done
                r.save()
                return
        counter += 1
        sleep(60)
    print('Send alert email')


def parse_guests(reservation):
    # refactor
    # first guest in first room
    traveler = reservation.reservation_rooms.first().room_guests.first().traveler
    guests = {
        'email': traveler.email,
        'phone': '{} {}'.format(
            traveler.phone_country_code,
            traveler.phone_number
        ),
        'customers': []
    }
    for r in reservation.reservation_rooms.all():
        guests['customers'].append(
            {
                'CustomerNames': get_customer_names(r)
            }
        )
    return guests


def card_payment(payment):
    reservation = Reservation.objects.prefetch_related(
        'reservation_rooms__room_guests'
    ).get(payment=payment)
    parsed_guests = parse_guests(reservation)
    payload =  {
        'BookingCode': reservation.booking_code,
        'CustomerDetails': parsed_guests['customers'],
        'ClientReferenceId': str(payment.id),
        'BookingReferenceId': str(reservation.id),
        'TotalFare': float(payment.subtotal),
        'EmailId': parsed_guests['email'],
        'PhoneNumber': parsed_guests['phone'],
        'BookingType': 'Voucher',
        'PaymentMode': 'NewCard',
        'PaymentInfo': {
            'CvvNumber': environ['CARD_CVV'],
            'CardNumber': environ['CARD_NUMBER'],
            'CardExpirationMonth': environ['CARD_EXPIRATION_MONTH'],
            'CardExpirationYear': environ['CARD_EXPIRATION_YEAR'],
            'CardHolderFirstName': environ['CARD_FIRST_NAME'],
            'CardHolderlastName': environ['CARD_LAST_NAME'],
            'BillingAmount': float(payment.subtotal),
            'BillingCurrency': 'USD',
            'CardHolderAddress': {
                'AddressLine1': environ['CARD_ADDRESS_LINE_1'],
                'AddressLine2': environ['CARD_ADDRESS_LINE_2'],
                'City': environ['CARD_CITY'],
                'PostalCode': environ['CARD_CP'],
                'CountryCode': environ['CARD_COUNTRY']
            }
        }
    }
    book = requests.post(BOOK_URL, headers=HEADERS, data=json.dumps(payload))
    save_log(PROVIDER_ID, BOOK_URL, payload, book.status_code, book.json())
    if book.status_code == 200:
        book_response = book.json()
        if book_response['Status']['Code'] == 200:
            reservation.booking_response = book_response
            reservation.policies_acceptance = True
            reservation.confirmation_number = book_response['ConfirmationNumber']
            reservation.reservation_status_id = 'c6cc1c43-7cae-408f-b4e4-4ebeac75d64b' # processing
            reservation.save()
            update_book_status.delay(reservation.id)
            return GenericResponse(
                data=PaymentSerializer(payment).data,
                status_code=status.HTTP_201_CREATED
            )
    return GenericResponse(
        data={'message': 'There was a problem with the booking process.'},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE
    )


def credit_payment(payment):
    reservation = Reservation.objects.prefetch_related(
        'reservation_rooms__room_guests'
    ).get(payment=payment)
    parsed_guests = parse_guests(reservation)
    payload =  {
        'BookingCode': reservation.booking_code,
        'CustomerDetails': parsed_guests['customers'],
        'ClientReferenceId': str(payment.id),
        'BookingReferenceId': str(reservation.id),
        'TotalFare': float(payment.subtotal),
        'EmailId': parsed_guests['email'],
        'PhoneNumber': parsed_guests['phone'],
        'BookingType': 'Voucher',
    }
    book = requests.post(BOOK_URL, headers=HEADERS, data=json.dumps(payload))
    save_log(PROVIDER_ID, BOOK_URL, payload, book.status_code, book.json())
    if book.status_code == 200:
        book_response = book.json()
        if book.json()['Status']['Code'] == 200:
            reservation.booking_response = book_response
            reservation.policies_acceptance = True
            reservation.confirmation_number = book_response['ConfirmationNumber']
            reservation.reservation_status_id = 'c6cc1c43-7cae-408f-b4e4-4ebeac75d64b' # processing
            reservation.save()
            update_book_status.delay(reservation.id)
            return GenericResponse(
                data=PaymentSerializer(payment).data,
                status_code=status.HTTP_201_CREATED
            )
    return GenericResponse(
        data={'message': 'There was a problem with the booking process.'},
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE
    )


def tbo_payment(payment):
    if PAYMENT_METHOD == 'Limit':
        response = credit_payment(payment)
    else:
        response = card_payment(payment)
    return response
