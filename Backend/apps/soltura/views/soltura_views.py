from dataclasses import asdict
from rest_framework.generics import GenericAPIView
from apps.soltura.models.soltura import Soltura
from rest_framework import status
from datetime import datetime
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from apps.soltura.dto.soltura_dtos import SolturaFiltroDTO,SolturaListInputDTO,CursorDTO,SolturaAnalyticsFiltroDTO,SolturaCreateDTO
from apps.soltura.services.soltura_services import SolturaListService,SolturaAnalyticsService,SolturaServiceCreate
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

class SolturaListBaseView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Soltura.objects.none()
    tipo_servico = None
    def get(self, request):
        column_filters = {}
        i = 0
        while f"columns[{i}][data]" in request.GET:
            col = request.GET.get(f"columns[{i}][data]")
            val = request.GET.get(f"columns[{i}][search][value]")
            column_filters[col] = val
            i += 1

        def parse_date(v):
            return datetime.strptime(v, "%Y-%m-%d").date() if v else None

        filtro = SolturaFiltroDTO(
            search=request.GET.get("search[value]"),
            status=request.GET.get("status"),
            data_inicio=parse_date(request.GET.get("data_inicio")),
            data_fim=parse_date(request.GET.get("data_fim")),
            limit=int(request.GET.get("length", 10)),
            column_filters=column_filters,
        )
        cursor = None
        if request.GET.get("cursor_id"):
            cursor = CursorDTO(
                id=int(request.GET["cursor_id"]),
                data_soltura=request.GET["cursor_date"],
            )

        input_dto = SolturaListInputDTO(
            tipo_servico=self.tipo_servico,
            filtro=filtro,
            cursor=cursor,
        )
        response = SolturaListService.listar(input_dto)

        return Response({
            "data": [asdict(i) for i in response.items],
            "recordsTotal": response.total,
            "recordsFiltered": response.total,
            "nextCursor": response.next_cursor,
        })
    
class RemocaoListView(SolturaListBaseView):
    tipo_servico = "Remoção"
class SeletivaListView(SolturaListBaseView):
    tipo_servico = "Seletiva"
class DomiciliarListView(SolturaListBaseView):
    tipo_servico = "Domiciliar"


#### VIEW BASE PRA GRAFICOS
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
####### VIEW PRA GRAFICOS POR TIPOS DE SERVICO 
class SolturaAnalyticsSeletivaView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_seletiva)
    tipo_servico = "Seletiva"

class SolturaAnalyticsDomiciliarView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_domiciliar)
    tipo_servico = "Domiciliar"

class SolturaAnalyticsRemocaoView(SolturaAnalyticsBaseView):
    filtro_fn = staticmethod(filtro_remocao)
    tipo_servico = "Remoção"