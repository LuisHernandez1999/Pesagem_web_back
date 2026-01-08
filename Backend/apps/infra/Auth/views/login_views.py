# apps/infra/Auth/views/login.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.infra.auth.dto.login_dto import LoginUserDTO
from apps.infra.auth.service.login import LoginService
from apps.infra.auth.exceptions.auth_exceptions import AuthException
from apps.infra.auth.adapters.login import login_user_adapter
class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        try:
            dto = login_user_adapter(request)
            result = LoginService.execute(dto)
            return Response(
                {
                    "message": "Login realizado com sucesso",
                    **result,
                },
                status=status.HTTP_200_OK,
            )
        except AuthException as exc:
            return Response(
                {"detail": str(exc)},
                status=exc.status_code,
            )
