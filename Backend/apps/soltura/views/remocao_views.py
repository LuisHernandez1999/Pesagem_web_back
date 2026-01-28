from dataclasses import asdict
from datetime import date
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.response import Response
from apps.soltura.models.soltura import Soltura
from apps.soltura.dto.remocao_dto  import SolturaFiltroDTO,SolturaCursorDTO,SolturaListInputDTO
from apps.soltura.services.remocao_services  import SolturaRemocaoStatsService,RemocaoListService


class SolturaRemocaoStatsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Soltura.objects.none()
    def get(self, request):
        dto = SolturaFiltroDTO(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
            status=request.query_params.get("status"),
        )
        resultado = SolturaRemocaoStatsService.executar(dto)
        return Response(resultado.__dict__)




class RemocaoListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Soltura.objects.none()
    def get(self, request):
        cursor = None
        if request.query_params.get("cursor_id") and request.query_params.get("cursor_data"):
            cursor = SolturaCursorDTO(
                id=int(request.query_params["cursor_id"]),
                data_soltura=date.fromisoformat(
                    request.query_params["cursor_data"]
                )
            )
        dto = SolturaListInputDTO(
            cursor=cursor,
            page_size=int(request.query_params.get("page_size", 20)),
            filters=request.query_params.get("filters"),
            search=request.query_params.get("search"),
            q=request.query_params.get("q"),
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )
        result = RemocaoListService.executar(dto)
        return Response({
            "items": [asdict(item) for item in result.items],
            "next_cursor": asdict(result.next_cursor) if result.next_cursor else None
        })
    
