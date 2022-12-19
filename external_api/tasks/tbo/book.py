from uuid import uuid4

from rest_framework import status

from common.response_class import GenericResponse

from agent.models import Agent

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer

from reservation.models import Reservation, Room, Guest

from external_api.tasks.tbo.common import PAYMENT_TYPE
from external_api.tasks.tbo.room_detail_prebook import tbo_get_room_prebook_details


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


# {
#   "BookingCode": "1247101!TB!1!TB!d6f7ec94-fd7a-4d62-b04b-2b9508b8c25d",
#   "CustomerDetails": [
#     {
#       "CustomerNames": [
#         {
#           "Title": "Mr",
#           "FirstName": "Shubham",
#           "LastName": "Gupta",
#           "Type": "Adult"
#         },
#         {
#           "Title": "Mr",
#           "FirstName": "Kunal",
#           "LastName": "Agrawal",
#           "Type": "Child"
#         }
#       ]
#     },
#     {
#       "CustomerNames": [
#         {
#           "Title": "Ms",
#           "FirstName": "Surbhi",
#           "LastName": "Jain",
#           "Type": "Adult"
#         },
#         {
#           "Title": "Ms",
#           "FirstName": "Anshu",
#           "LastName": "Rawat",
#           "Type": "Child"
#         }
#       ]
#     }
#   ],
#   "BookingType": "Voucher",
#   "PaymentMode": "SavedCard",
#   "PaymentInfo": {
#     "CvvNumber": "123"
#   },
#   "ClientReferenceId": "1626265961573-16415097",
#   "BookingReferenceId": "AVw123218",
#   "TotalFare": 43.2,
#   "EmailId": "apisupport@tboholidays.com",
#   "PhoneNumber": "918448780621"
# }


def tbo_payment(payment):
    return GenericResponse(
        data=PaymentDetailSerializer(payment).data,
        status_code=status.HTTP_201_CREATED
    )
