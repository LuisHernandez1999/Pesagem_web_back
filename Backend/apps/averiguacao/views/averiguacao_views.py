from dataclasses import asdict
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.generics import GenericAPIView
from apps.averiguacao.models.averiguacao import Averiguacao
from apps.averiguacao.services.averiguacao_services import (
    AveriguacaoEstatisticasSemanaService,
    AveriguacaoServiceCreate
)
from apps.averiguacao.dto.averiguacao_dto import (
    AveriguacaoEstatisticasSemanaRequestDTO,
    AveriguacaoCreateRequestDTO
)


class AveriguacaoCreateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Averiguacao.objects.none()

    def post(self, request):
        try:
            dto =  AveriguacaoCreateRequestDTO(
                tipo_servico=request.data.get("tipo_servico"),
                pa_da_averiguacao=request.data.get("pa_da_averiguacao"),
                rota_averiguada_id=request.data.get("rota_averiguada_id"),
                averiguador=request.data.get("averiguador"),
                formulario=request.data.get("formulario"),
            )

            averiguacao_id = AveriguacaoServiceCreate.create(dto)

            return Response(
                {"id": averiguacao_id},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class AveriguacaoEstatisticasSemanaApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Averiguacao.objects.none()
    def get(self, request):
        dto = AveriguacaoEstatisticasSemanaRequestDTO(
            tipo_servico=request.query_params.get("tipo_servico"),
            pa=request.query_params.get("pa"),
            turno=request.query_params.get("turno"),
            data_inicio=request.query_params.get("data_inicio"),
            data_fim=request.query_params.get("data_fim"),
        )
        service = AveriguacaoEstatisticasSemanaService()
        result = service.execute(dto)
        return Response(asdict(result))