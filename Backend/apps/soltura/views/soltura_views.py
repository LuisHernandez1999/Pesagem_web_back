from rest_framework.generics import GenericAPIView
from apps.soltura.models.soltura import Soltura
from dataclasses import asdict
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.soltura.dto.soltura_dtos import SolturaCreateDTO
from apps.soltura.services.soltura_services import SolturaServiceCreate
from apps.soltura.views.soltura_base_views import SolturaAnalyticsBaseView
from apps.soltura.utils.filters_utils import filtro_remocao,filtro_seletiva,filtro_domiciliar
from apps.soltura.dto.soltura_dtos import CursorDTO
from apps.soltura.services.soltura_services import SolturaResumoService

class SolturaListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Soltura.objects.none()

    def get(self, request):
        termo = request.GET.get("search")
        tipo_servico = request.GET.get("tipo_servico")  # 👈 AQUI
        cursor = None

        if request.GET.get("cursor_id"):
            cursor = CursorDTO(
                id=int(request.GET["cursor_id"]),
                data_soltura=request.GET.get("cursor_date"),
            )

        response = SolturaResumoService.executar(
            termo=termo,
            cursor=cursor,
            tipo_servico=tipo_servico,  # 👈 E AQUI
        )

        return Response({
            "items": response.items,
            "total": response.total,
            "next_cursor": response.next_cursor,
        })








class SolturaAnalyticsSeletivaView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_seletiva)
    tipo_servico = "Seletiva"

class SolturaAnalyticsDomiciliarView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_domiciliar)
    tipo_servico = "Domiciliar"

class SolturaAnalyticsRemocaoView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_remocao)
    tipo_servico = "Remoção"