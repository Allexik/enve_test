from rest_framework.exceptions import APIException


class FieldException(APIException):
    status_code = 500
    default_detail = 'Field does not exist'
    default_code = 'field_error'


