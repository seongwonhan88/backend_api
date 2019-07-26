from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyActive(APIException):
    default_detail = {'error': ['User already active']}
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class EmailNotFound(APIException):
    default_detail = {'error': ['Email not found']}
    status_code = status.HTTP_404_NOT_FOUND

