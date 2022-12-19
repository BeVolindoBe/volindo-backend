from uuid import uuid4

from rest_framework import status

from common.response_class import GenericResponse

from agent.models import Agent

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer

from reservation.models import Reservation, Room, Guest

from external_api.tasks.tbo.common import PAYMENT_TYPE


def tbo_book(data, user):
    payment = Payment.objects.create(
        agent=Agent.objects.get(user=user),
        payment_type_id=PAYMENT_TYPE,
        commission=data['payment']['commission'],
        subtotal=data['payment']['subtotal'],
        total=data['payment']['total']
    )
    reservation = Reservation.objects.create(
        payment=payment,
        hotel_id=data['hotel_id'],
        search_parameters=data['filters'],
        booking_code=data['booking_code'],
        policies=data['policies']
    )
    rooms_list = []
    guests_list = []
    for room in data['rooms']:
        room_id = str(uuid4())
        rooms_list.append(
            Room(
                id=room_id,
                reservation=reservation,
                name=room['name']
            )
        )
        for guest in room['guests']:
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


def tbo_payment(payment):
    return GenericResponse(
        data=PaymentDetailSerializer(payment).data,
        status_code=status.HTTP_201_CREATED
    )
