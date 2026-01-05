# apps/infra/Auth/views/login.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.infra.Auth.dto.login_dto import LoginUserDTO
from apps.infra.Auth.service.login import LoginService
from apps.infra.Auth.exceptions.auth_exceptions import AuthException


class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            dto = LoginUserDTO(
                email=request.data["email"],
                password=request.data["password"],
            )

            user = LoginService.execute(dto)

            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )

        except KeyError:
            return Response(
                {"detail": "email e password são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except AuthException as exc:
            return Response(
                {"detail": exc.message},
                status=exc.status_code,
            )
