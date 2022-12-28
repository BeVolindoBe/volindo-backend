import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.logs import save_log
from external_api.tasks.tmx.common import(
    HEADERS, SEARCH_URL, PROVIDER_ID
)


def parse_baggage(data):
    return {
        'baggage': data['Baggage'] if 'Baggage' in data else None,
        'cabin_baggage': data['CabinBaggage'] if 'CabinBaggage' in data else None,
    }


def parse_destination(data):
    return {
        'airport_code': data['AirportCode'],
        'airport_name': data['AirportName'],
        'city_name': data['CityName'],
        'date_time': data['DateTime'],
    }


def parse_origin(data):
    return {
        'airport_code': data['AirportCode'],
        'airport_name': data['AirportName'],
        'city_name': data['CityName'],
        'date_time': data['DateTime'],
    }


def parse_flights(flights):
    # first element of the array includes the going flights,
    # second element contains the returning flights
    flights = []
    for x in range(len(flights[0])): # going
        for y in range(len(flights[1])): # returning
            flights.append(
                {
                    'going': {
                        'flights': [
                            {
                                'airline_code': f['OperatorCode'],
                                'airline_image': 'http://18.188.80.180/apiTravelsb2b/airlines/AM.png',
                                'airline_name': 'OperatorName',
                                'baggage': parse_baggage(f['Attr']),
                                'class': f['Attr'],
                                'destination': parse_destination(f['Destination']),
                                'duration': f['Duration'],
                                'flight_number': f['FlightNumber'],
                                'origin': parse_origin(f['Origin'])
                            } for f in flights[0][x]['FlightDetails']['Details'][0]
                        ],
                        'stops': len(flights[0][x]['FlightDetails']['Details'][0]),
                        'total_duration': 140,
                    },
                    'isRefundable': False,
                    'points': 222.84,
                    'price': {
                        'currency': 'USD',
                        'markUp': 0,
                        'offeredPrice': 151.68,
                        'totalPrice': 151.68,
                        'totalPriceAdults': 151.68,
                        'totalPriceChildren': None,
                        'totalPriceInfants': None,
                    },
                    'resultToken': 'c2b03b9a55448093852cef9ab15431df*_*9*_*n3GpqdDwKZkQOOzU',
                    'returning': [
                        {
                            'flights': [
                                {
                                    'airlineCode': 'AM',
                                    'airlineImage': 'http://18.188.80.180/apiTravelsb2b/airlines/AM.png',
                                    'airlineName': 'Aeromexico',
                                    'baggage': {'baggage': '0PC', 'cabin': '7 Kg'},
                                    'class': 'Y',
                                    'destination': {
                                        'airportCode': 'MEX',
                                        'airportName': 'Mexico City',
                                        'city': 'Mexico City',
                                        'dateTime': '2023-01-28 08:55:00',
                                    },
                                    'duration': '154',
                                    'flightNumber': '507',
                                    'origin': {
                                        'airportCode': 'CUN',
                                        'airportName': 'Cancun',
                                        'city': 'Cancun',
                                        'dateTime': '2023-01-28 07:21:00',
                                    },
                                }
                            ],
                            'stops': 0,
                            'totalDuration': 154,
                        }
                    ],
                    'totalAdults': 1,
                    'totalChildren': 0,
                    'totalDuration': 294,
                    'totalInfant': 0
                }
            )
    return flights


@shared_task
def tmx_search_flights(results_id, filters):
    payload = {
        'AdultCount': f"{filters['adults']}",
        'ChildCount': f"{filters['children']}",
        'InfantCount': f"{filters['infants']}",
        'JourneyType': f"{filters['flight_type']}",
        'PreferredAirlines': [''],
        'CabinClass': f"{filters['flight_class']}",
        'Segments': [
            {
                'Origin': 'BLR',
                'Destination': 'MAA',
                'DepartureDate': '2023-01-04T00:00:00',
                'ReturnDate': '2023-01-10T00:00:00'
            }
        ]
    }
    response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
    save_log(PROVIDER_ID, SEARCH_URL, payload, response.status_code, response.json())
    results = json.loads(cache.get(results_id))
    if response.status_code == 200:
        response_data = response.json()
        if response_data['Status'] == 1:
            results['flights'] = parse_flights(response_data['Search']['FlightDataList']['JourneyList'])
    results['status'] = 'update'
    cache.set(results_id, json.dumps(results), 900)
