# apps/infra/auth/views/register_user.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.infra.auth.adapters.register import register_user_adapter
from apps.infra.auth.adapters.register import register_by_invite_adapter
from apps.infra.auth.service.register_user import RegisterUserService
from apps.infra.auth.exceptions.auth_exceptions import AuthException
from apps.infra.auth.service.register_user import (
    RegisterUserByInviteService
)
class RegisterUserAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        try:
            user = RegisterUserService.execute(
                register_user_adapter(request)
            )
            return Response(
                {
                    "message": "Usuário criado com sucesso",
                    "user": {"id": user.id, "email": user.email},
                },
                status=status.HTTP_201_CREATED,
            )
        except AuthException as exc:
            return Response(
                {"detail": str(exc)},
                status=getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
            )


class RegisterByInviteAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            dto = register_by_invite_adapter(request)
            user = RegisterUserByInviteService.execute(dto)

            return Response(
                {
                    "message": "Usuário criado com sucesso",
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )

        except AuthException as exc:
            return Response(
                {"detail": exc.detail},
                status=exc.status_code,
            )