from django.test import Client


FIXTURES = [
    'user/fixtures/users.yaml',
    # 'agent/fixtures/agents.yaml',
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
    'airport/fixtures/airports.yaml',
]

USER_ID = '87a69f31-c564-4079-be07-759e58c952dd'
