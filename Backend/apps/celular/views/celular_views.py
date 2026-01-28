from dataclasses import asdict
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.response import Response
from rest_framework import status
from apps.celular.models.celular import Celular
from apps.celular.dto.celular_dto import CelularCreateDTO
from apps.celular.services.celular_service import CelularCreateService
from apps.celular.exceptions.celular_exceptions import CelularException


class CelularCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Celular.objects.none()
    def post(self, request):
        try:
            dto = CelularCreateDTO(
                numero=request.data.get("numero"),
                ativo=request.data.get("ativo", True),
                modelo=request.data.get("modelo"),
                fabricante=request.data.get("fabricante"),
                garagem_atual=request.data.get("garagem_atual"),
                codigo_imei=request.data.get("codigo_imei"),
                apelido=request.data.get("apelido"),
            )
            response_dto = CelularCreateService.execute(dto)
            return Response(
                asdict(response_dto),
                status=status.HTTP_201_CREATED,
            )
        except CelularException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
