# apps/infra/Auth/views/register_user.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.infra.auth.mappers.user_mappers.post_user_mapper import (
    register_user_mapper,
)
from apps.infra.auth.service.register_user import RegisterUserService
from apps.infra.auth.exceptions.auth_exceptions import AuthException


class RegisterUserAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            dto = register_user_mapper(request)
            user = RegisterUserService.execute(dto)

            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )

        except AuthException as exc:
            return Response(
                {"detail": exc.message},
                status=exc.status_code,
            )
