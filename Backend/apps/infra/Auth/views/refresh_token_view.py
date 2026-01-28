from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.infra.auth.dto.refresh_token import RefreshTokenDTO
from apps.infra.auth.service.refresh_token import RefreshTokenService


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        dto = RefreshTokenDTO(refresh=request.data.get("refresh"))
        data = RefreshTokenService.execute(dto)
        return Response(data, status=status.HTTP_200_OK)