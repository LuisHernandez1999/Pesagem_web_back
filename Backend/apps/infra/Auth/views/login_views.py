from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.infra.auth.service.login import LoginService
from apps.infra.auth.exceptions.auth_exceptions import AuthException
from apps.infra.auth.adapters.login import login_user_adapter


@method_decorator(csrf_exempt, name="dispatch")
class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

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
