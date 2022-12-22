from django.test import Client


FIXTURES = [
    'catalogue/fixtures/catalogues.yaml',
    'catalogue/fixtures/agent_status.yaml',
    'catalogue/fixtures/agent_subscriptions.yaml',
    'catalogue/fixtures/traveler_status.yaml',
    'catalogue/fixtures/countries.yaml',
    'catalogue/fixtures/api_providers.yaml',
    'catalogue/fixtures/destinations.yaml',
    'catalogue/fixtures/payment_types.yaml',
    'catalogue/fixtures/reservation_status.yaml',
    'hotel/fixtures/hotels.yaml',
    'hotel/fixtures/hotel_amenities.yaml',
    'hotel/fixtures/hotel_pictures.yaml',
]


def get_token():
    client = Client()
    data = {
        'first_name': 'Travel',
        'last_name': 'Agent',
        'username': 'user@example.com',
        'email': 'user@example.com',
        'password': 'W1D78#Ae9O5r',
        'password2': 'W1D78#Ae9O5r',
    }
    client.post('/accounts/register/', data=data)
    data = {
        'username': 'user@example.com',
        'password': 'W1D78#Ae9O5r'
    }
    response = client.post('/token/', data=data)
    return response.json()['access']
