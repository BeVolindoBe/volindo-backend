import json
import requests
from django.core.cache import cache
from celery import shared_task
from external_api.tasks.tbo.common import HEADERS, HOST, PROVIDER_ID
from hotel.models import Hotel
from django.forms.models import model_to_dict

def parse_rooms(rooms_list) -> list:
	rooms = []
	for room in rooms_list:
		rooms.append({
			'Adults': room['number_of_adults'],
			'Children': len(room['children_age']),
			'ChildrenAges': room['children_age']
		})
	return rooms

def getHotelCodes(destination) -> list:
	hotels = Hotel.objects.filter(destination=destination)
	ids = [hotel.external_id for hotel in hotels]
	return ','.join(ids)

def price(elem):
	return elem.get('price')

@shared_task
def search_tbo(results_id, filters):
	url = f'{HOST}/Search'
	parsed_rooms = parse_rooms(filters['rooms'])
	hotelCodes = getHotelCodes(filters['destination'])
	payload = {
		'CheckIn': filters['check_in'], # format YYYY-mm-dd
		'CheckOut': filters['check_out'], # format YYYY-mm-dd
		'HotelCodes': hotelCodes,
		'GuestNationality': filters['nationality'],
		'PaxRooms': parsed_rooms,
		'ResponseTime': 23,
		'IsDetailedResponse': False
	}
	response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
	if response.status_code == 200:
		response = response.json()
		prices = {}
		for hotel in response['HotelResult']:
			prices[hotel['HotelCode']] = hotel['Rooms'][0]['TotalFare'] 
		searchedHotels = Hotel.objects.prefetch_related('hotel_pictures').filter(provider_id='a33ba54c-34f9-4f1a-9d87-0d85a4cfdeba', external_id__in=list(prices.keys()))
		tempHotels = []
		for hotel in searchedHotels:
			temp = model_to_dict(hotel)
			temp['destination'] = str(temp['destination'])
			temp['provider'] = str(temp['provider'])
			temp['latitude'] = float(temp['latitude'])
			temp['longitude'] = float(temp['longitude'])
			temp['price'] = prices[temp['external_id']]
			tempHotels.append(temp)
		results = json.loads(cache.get(results_id))
		results['status'] = 'update'
		results['hotels'].extend(tempHotels)
		results['hotels'].sort(key=price)
		cache.set(results_id, json.dumps(results), 18000)














