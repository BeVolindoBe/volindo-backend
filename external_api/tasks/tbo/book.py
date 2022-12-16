from rest_framework import status

from common.response_class import GenericResponse


def tbo_book(data):
    return GenericResponse(
        data={
            'message': 'OK'
        },
        status_code=status.HTTP_201_CREATED
    )
