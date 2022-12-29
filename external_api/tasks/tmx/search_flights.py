import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.logs import save_log
from external_api.tasks.tmx.common import(
    HEADERS, SEARCH_URL, PROVIDER_ID, FLIGHT_DICT
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


def parse_details(data):
    details = {
        'flights': [],
        'stops': len(data) - 1,
        'duration': 0
    }
    for f in data:
        details['duration'] += f['Duration']
        details['flights'].append(
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
            }
        )
    return details


def return_flight(flights_data):
    # first element of the array includes the going flights,
    # second element contains the returning flights
    flights = []
    going_flights = flights_data[0]
    returning_flights = flights_data[1]
    for x in range(len(going_flights)): # going
        for y in range(len(returning_flights)): # returning
            going_details = parse_details(going_flights[x]['FlightDetails']['Details'][0])
            returning_details = parse_details(returning_flights[y]['FlightDetails']['Details'][0])
            flights.append(
                {
                    'going': {
                        'flights': going_details['flights'],
                        'stops': going_details['stops'],
                        'total_duration': going_details['duration'],
                        'result_token': going_flights[x]['ResultToken'],
                        'is_refundable': going_flights[x]['Attr']['IsRefundable'],
                        'price': going_flights[x]['Price']['TotalDisplayFare']
                    },
                    'price': {
                        'currency': 'USD',
                        'total_price': going_flights[x]['Price']['TotalDisplayFare'] if returning_flights is None else (
                            going_flights[x]['Price']['TotalDisplayFare'] +
                            returning_flights[y]['Price']['TotalDisplayFare']
                        ),
                    },
                    'returning': [
                        {
                            'flights': returning_details['flights'],
                            'stops': returning_details['stops'],
                            'total_duration': returning_details['duration'],
                            'result_token': returning_flights[y]['ResultToken'],
                            'is_refundable': returning_flights[y]['Attr']['IsRefundable'],
                            'price': returning_flights[y]['Price']['TotalDisplayFare']
                        }
                    ] if returning_flights is not None else []
                }
            )
    return flights


def one_way_flight(flights_data):
    flights = []
    going_flights = flights_data[0]
    for x in range(len(going_flights)): # going
        going_details = parse_details(going_flights[x]['FlightDetails']['Details'][0])
        flights.append(
            {
                'going': {
                    'flights': going_details['flights'],
                    'stops': going_details['stops'],
                    'total_duration': going_details['duration'],
                    'result_token': going_flights[x]['ResultToken'],
                    'is_refundable': going_flights[x]['Attr']['IsRefundable'],
                    'price': going_flights[x]['Price']['TotalDisplayFare']
                },
                'price': {
                    'currency': 'USD',
                    'total_price': going_flights[x]['Price']['TotalDisplayFare']
                },
                'returning': []
            }
        )
    return flights


@shared_task
def tmx_search_flights(results_id, filters):
    payload = {
        'AdultCount': f"{filters['adults']}",
        'ChildCount': f"{filters['children']}",
        'InfantCount': f"{filters['infants']}",
        'JourneyType': f"{FLIGHT_DICT[filters['flight_type']]}",
        'PreferredAirlines': [''],
        'CabinClass': f"{FLIGHT_DICT[filters['flight_class']]}",
        'Segments': [
            {
                'Origin': filters['origin'],
                'Destination': filters['destination'],
                'DepartureDate': f"{filters['departure_date']}T00:00:00",
                'ReturnDate': f"{filters['return_date']}T00:00:00",
            }
        ]
    }
    response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
    save_log(PROVIDER_ID, SEARCH_URL, payload, response.status_code, response.json())
    results = json.loads(cache.get(results_id))
    if response.status_code == 200:
        response_data = response.json()
        if response_data['Status'] == 1:
            if filters['flight_type'] == 'one_way':
                    results['flights'] = one_way_flight(response_data['Search']['FlightDataList']['JourneyList'])
            else:
                results['flights'] = return_flight(response_data['Search']['FlightDataList']['JourneyList'])
    results['status'] = 'update'
    cache.set(results_id, json.dumps(results), 900)
