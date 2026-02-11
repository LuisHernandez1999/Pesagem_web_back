from dataclasses import asdict
from rest_framework.generics import GenericAPIView
from apps.soltura.models.soltura import Soltura
from datetime import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.soltura.dto.soltura_dtos import SolturaAnalyticsFiltroDTO
from apps.soltura.services.soltura_services import SolturaAnalyticsService


class SolturaAnalyticsBaseView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Soltura.objects.none()
    filtro_fn = None  # Deve ser definido na subclasse
    tipo_servico = None  # Opcional, para deixar mais explícito

    def get(self, request):
        def parse_date(v):
            return datetime.strptime(v, "%Y-%m-%d").date() if v else None
        # Usa filtro_fn da view para criar o DTO
        dto = SolturaAnalyticsFiltroDTO(
            tipo_servico=self.tipo_servico or getattr(self.filtro_fn, "__name__", "Desconhecido").replace("filtro_", "").capitalize(),
            filtro_fn=self.filtro_fn,
            status=request.GET.get("status"),
            data_inicio=parse_date(request.GET.get("data_inicio")),
            data_fim=parse_date(request.GET.get("data_fim")),
        )
        data = SolturaAnalyticsService.executar(dto)
        return Response(data)