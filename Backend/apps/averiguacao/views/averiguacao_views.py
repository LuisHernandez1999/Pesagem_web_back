from dataclasses import asdict
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.generics import GenericAPIView
from apps.averiguacao.models.averiguacao import Averiguacao
from apps.averiguacao.services.averiguacao_services import (
    AveriguacaoEstatisticasSemanaService,
)
from apps.averiguacao.dto.averiguacao_dto import (
    AveriguacaoEstatisticasSemanaRequestDTO,
)

class AveriguacaoEstatisticasSemanaView(GenericAPIView):
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