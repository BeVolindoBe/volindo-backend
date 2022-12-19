from os import environ

from uuid import uuid4

from rest_framework import status

from common.response_class import GenericResponse

from agent.models import Agent

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer

from reservation.models import Reservation, Room, Guest

from external_api.tasks.tbo.common import PAYMENT_TYPE
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
                price=room_details['rooms']['rooms_details'][x]['price']
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
    return GenericResponse(
        data=PaymentSerializer(payment).data,
        status_code=status.HTTP_201_CREATED
    )


def get_customer_names(room):
    return [
        {
            'Title': TITLE_DICT[g['traveler']['title']][0],
            'FirstName': g['traveler']['first_name'],
            'LastName': g['traveler']['last_name'],
            'Type': TITLE_DICT[g['traveler']['title']][1]
        } for g in room['guests']
    ]


def parse_guests(reservation):
    data = {
        'email': reservation['rooms'][0]['guests'][0]['traveler']['email'],
        'phone': '{} {}'.format(
            reservation['rooms'][0]['guests'][0]['traveler']['phone_country_code'],
            reservation['rooms'][0]['guests'][0]['traveler']['phone_number']
        ),
        'customers': []
    }
    for r in reservation['rooms']:
        data['customers'].append(
            {
                'CustomerNames': get_customer_names(r)
            }
        )
    return data


def tbo_payment(payment):
    payment_data = PaymentDetailSerializer(payment).data
    parsed_guests = parse_guests(parse_guests(payment_data['reservation']))
    payload =  {
        'BookingCode': payment_data['reservation']['booking_code'],
        'CustomerDetails': parsed_guests['customers'],
        'ClientReferenceId': payment_data['id'],
        'BookingReferenceId': payment_data['reservation']['id'],
        'TotalFare': payment_data['subtotal'],
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
            'BillingAmount': payment_data['subtotal'],
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
    print(payload)
    return GenericResponse(
        data=PaymentDetailSerializer(payment).data,
        status_code=status.HTTP_201_CREATED
    )
