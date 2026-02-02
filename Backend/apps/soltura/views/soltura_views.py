from rest_framework.generics import GenericAPIView
from apps.soltura.models.soltura import Soltura
from rest_framework import status
from datetime import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.soltura.dto.soltura_dtos import SolturaCreateDTO
from apps.soltura.services.soltura_services import SolturaServiceCreate
from apps.soltura.views.soltura_base_views import SolturaListBaseView,SolturaAnalyticsBaseView
from apps.soltura.utils.filters_utils import filtro_remocao,filtro_seletiva,filtro_domiciliar




class SolturaCreateView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Soltura.objects.none()
    def post(self, request):
        try:
            data = request.data.copy()

            data["hora_entrega_chave"] = datetime.strptime(
                data["hora_entrega_chave"], "%H:%M"
            ).time()

            data["hora_saida_frota"] = datetime.strptime(
                data["hora_saida_frota"], "%H:%M"
            ).time()

            dto = SolturaCreateDTO(**data)
            soltura_id = SolturaServiceCreate.create(dto)

            return Response(
                {"id": soltura_id},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"erro": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )




class RemocaoListView(SolturaListBaseView):
    tipo_servico = "Remoção"
class SeletivaListView(SolturaListBaseView):
    tipo_servico = "Seletiva"
class DomiciliarListView(SolturaListBaseView):
    tipo_servico = "Domiciliar"



class SolturaAnalyticsSeletivaView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_seletiva)
    tipo_servico = "Seletiva"

class SolturaAnalyticsDomiciliarView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_domiciliar)
    tipo_servico = "Domiciliar"

class SolturaAnalyticsRemocaoView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_remocao)
    tipo_servico = "Remoção"