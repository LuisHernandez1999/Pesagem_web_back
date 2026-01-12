from rest_framework import status


class CooperativaException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Erro na cooperativa"


class CooperativaAlreadyExists(CooperativaException):
    detail = "Cooperativa já cadastrada"
    status_code = status.HTTP_409_CONFLICT
