from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.cooperativa.dto.cooperativa_dto import CreateCooperativaDTO
from apps.cooperativa.services.cooperativa_services import CreateCooperativaService
from apps.cooperativa.excepetions.cooperativa_exceptions import CooperativaException
from apps.cooperativa.models.cooperativa import Cooperativa
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView


class CooperativaCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Cooperativa.objects.none()

    def post(self, request):
        try:
            dto = CreateCooperativaDTO(**request.data)
            cooperativa_id = CreateCooperativaService.create(dto)

            return Response(
                {"cooperativa criada com sucesso ": cooperativa_id},
                status=status.HTTP_201_CREATED,
            )

        except TypeError:
            return Response(
                {"detail": "Payload inválido"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        except CooperativaException as e:
            return Response(
                {"detail": e.detail},
                status=e.status_code,
            )
