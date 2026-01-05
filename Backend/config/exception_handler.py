from rest_framework.response import Response
from rest_framework import status

from apps.infra.Auth.exceptions.auth_exceptions import AuthException


def custom_exception_handler(exc, context):
    if isinstance(exc, AuthException):
        return Response(
            {"error": exc.default_detail},
            status=exc.status_code,
        )

    return None  
