from uuid import uuid4

import json

import requests

from django.core.cache import cache

from celery import shared_task

from hotel.models import Hotel, HotelPicture

from external_api.tasks.rakuten.common import HEADERS, STATIC_HOST, IMAGE_HOST, PROVIDER_ID


def save_data(hotels):
    # refactor
    image_url = url = IMAGE_HOST + '/{}/{}' # hotel id then image file name
    ids = Hotel.objects.filter(provider_id=PROVIDER_ID, external_id__in=hotels.keys())
    for h in ids:
        hotels.pop(h)
    for k, v in hotels.items():
        images = []
        hotel_id = str(uuid4())
        hotel = Hotel.objects.create(
            id=hotel_id,
            destination=None,
            provider_id=PROVIDER_ID,
            external_id=v['id'],
            hotel_name=v['name'],
            country_code=v['country_code'],
            city=v['city'],
            stars=v['rating'],
            latitude=v['latitude'],
            longitude=v['longitude'],
            address=f'{v["state_province"]}, {v["city"]}',
            description=v['description'],
        )
        if 'hero_images' in v:
            try:
                images.append(
                    HotelPicture(
                        hotel=hotel,
                        image_type='P',
                        url=image_url.format(k, v['hero_image'][0]['links']['s']['href'])       
                    )
                )
            except Exception as e:
                print('Error creating hero image: ', e)
        if 'images' in v:
            for i in v['images']:
                try:
                    images.append(
                        HotelPicture(
                            hotel=hotel,
                            image_type='A',
                            url=image_url.format(k, i['links']['l']['href'])
                        )
                    )
                except Exception as e:
                    print('Error creating image: ', e)
        HotelPicture.objects.bulk_create(images)


def get_properties():
    url = STATIC_HOST + '/my-property-list'
    properties = requests.get(
        url=url,
        headers=HEADERS
    )
    return [
        p['property_code'] for p in properties.json()['my_property_list']
    ]


def get_details(properties_codes):
    url = STATIC_HOST + '/properties?extends=long%2Cimages%2Crooms%2Cfacilities'
    body = {
        'property_codes': properties_codes
    }
    details = requests.post(
        url=url,
        headers=HEADERS,
        data=json.dumps(body)
    )
    return details.json()


def rakuten_data():
    proprties = get_properties()
    hotels = get_details(properties_codes=proprties)
    save_data(hotels=hotels)
