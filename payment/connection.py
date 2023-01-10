from os import environ

import stripe


MODE = environ.get('STRIPE_MODE')
SUCCESS_URL = environ.get('STRIPE_SUCCESS_URL')
PRICE = environ.get('STRIPE_ITEM_PRICE')
QUANTITY = environ.get('STRIPE_ITEM_QUANTITY')
URL = environ.get('STRIPE_URL')
KEY = environ.get('STRIPE_KEY')


def get_stripe_session():
    stripe.api_key = 'sk_test_51M0AYpJLqNE3DWQ6UJQ7S4bxtmYKZJyRwokDelUSvRiws5ZUjmzFouo1llhQUqjO15pYB7nzbvdY10jMnzEzcbgK00oymrIfjl'
    return stripe.checkout.Session.create(
        success_url=SUCCESS_URL,
        cancel_url=SUCCESS_URL,
        line_items=[
            {
                'price': PRICE,
                'quantity': int(QUANTITY),
            },
        ],
        mode='subscription',
    )
