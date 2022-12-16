from rest_framework import status

from common.response_class import GenericResponse


def tbo_book(data):
    return GenericResponse(
        data=data,
        status_code=status.HTTP_201_CREATED
    )
