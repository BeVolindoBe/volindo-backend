from os import environ

import requests

from rest_framework import status

from common.response_class import GenericResponse

from external_api.tasks.tbo.book import tbo_payment

from payment.models import Payment


STRIPE_PAYMENT_TOKEN_URL=environ['STRIPE_PAYMENT_TOKEN_URL']
STRIPE_PAYMENT_URL=environ['STRIPE_PAYMENT_URL']
STRIPE_PAYMENT_AUTH=environ['STRIPE_PAYMENT_AUTH']


HEADERS = {
    'Authorization': STRIPE_PAYMENT_AUTH,
    'Content-Type': 'application/x-www-form-urlencoded'
}


def validate_card(card_details):
    payload = 'card%5Bnumber%5D={}&card%5Bexp_month%5D={}&card%5Bexp_year%5D={}&card%5Bcvc%5D={}'.format(
        card_details['card_number'],
        card_details['exp_date'].split('/')[0],
        card_details['exp_date'].split('/')[1],
        card_details['cvv']
    )
    response = requests.post(
        STRIPE_PAYMENT_TOKEN_URL,
        data=payload,
        auth=(STRIPE_PAYMENT_AUTH, '')
    )
    if response.status_code == 200:
        return response.json()['id']
    else:
        return False


def execute_payment(amount, token):
    payload = 'amount={}&currency=USD&source={}&description=Volindo%20Book'.format(
        int(float(amount)*100),
        token
    )
    response = requests.post(
        STRIPE_PAYMENT_URL,
        data=payload,
        auth=(STRIPE_PAYMENT_AUTH, '')
    )
    if response.status_code == 200:
        return response.json()
    return False


def pay_reservation(payment_id, card_details):
    card_token = validate_card(card_details=card_details)
    if card_token is False:
        return GenericResponse(
            data={'message': 'Invalid card information.'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    payment = Payment.objects.get(id=payment_id)
    confirmation = execute_payment(payment.total, card_token)
    if confirmation is False:
        return GenericResponse(
            data={'message': 'There was a problem with the payment method.'},
            status_code=status.HTTP_402_PAYMENT_REQUIRED
        )
    payment.response_data = confirmation
    payment.save()
    book = tbo_payment(payment)
    if book is False:
        return GenericResponse(
            data={'message': 'There was a problem with the booking process.'},
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    return book
