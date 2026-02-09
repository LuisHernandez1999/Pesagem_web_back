from rest_framework.response import Response
from django.http import HttpResponse
from dataclasses import asdict
from datetime import datetime, timedelta,date
import orjson
from rest_framework.permissions import IsAuthenticated
from rest_framework_orjson.renderers import ORJSONRenderer
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.generics import GenericAPIView
from apps.averiguacao.models.averiguacao import Averiguacao
from apps.averiguacao.services.averiguacao_services import (
    AveriguacaoSemanaService,
    CriarAveriguacaoService,
    AveriguacaoListService,
    AveriguacaoByIDService,
    AveriguacaoReportService
)
from apps.averiguacao.dto.averiguacao_dto import (
    AveriguacaoCreateRequestDTO,
    AveriguacaoCreateResponseDTO
)


class AveriguacaoCreateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Averiguacao.objects.none()

    def post(self, request):
        try:
            dto = AveriguacaoCreateRequestDTO(
                rota_id=request.data.get("rota_averiguada"),
                tipo_servico=request.data.get("tipo_servico"),
                pa_da_averiguacao=request.data.get("pa_da_averiguacao"),
                averiguador=request.data.get("averiguador"),
                formulario=request.data.get("formulario"),
                imagem1=request.data.get("imagem1"),
                imagem2=request.data.get("imagem2"),
                imagem3=request.data.get("imagem3"),
                imagem4=request.data.get("imagem4"),
                imagem5=request.data.get("imagem5"),
                imagem6=request.data.get("imagem6"),
                imagem7=request.data.get("imagem7"),
            )

            response_dto: AveriguacaoCreateResponseDTO = CriarAveriguacaoService.executar(dto)
            return HttpResponse(
                content=orjson.dumps(response_dto.__dict__),  
                content_type="application/json",
                status=201
            )

        except Exception as e:
            return HttpResponse(
                content=orjson.dumps({"erro": str(e)}),
                content_type="application/json",
                status=400
            )
        




class AveriguacaoEstatisticasSemanaApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    renderer_classes = (ORJSONRenderer,)
    queryset = Averiguacao.objects.none()

    def get(self, request):
        data_inicio_str = request.query_params.get("data_inicio")
        data_fim_str = request.query_params.get("data_fim")
        pa = request.query_params.get("pa")
        turno = request.query_params.get("turno")
        tipo_servico = request.query_params.get("tipo_servico", "Remoção")

        
        dia_semana = None
        if data_inicio_str and data_fim_str:
            try:
                dia_semana = {
                    "inicio": date.fromisoformat(data_inicio_str),
                    "fim": date.fromisoformat(data_fim_str),
                }
            except ValueError:
                return Response(
                    data=orjson.dumps({"erro": "Formato de data inválido. Use YYYY-MM-DD."}),
                    status=400,
                    content_type="application/json"
                )
        result = AveriguacaoSemanaService.get_averiguacao_service(
            pa=pa,
            turno=turno,
            servico=tipo_servico,
            dia_semana=dia_semana
        )
        return Response(orjson.loads(orjson.dumps(result)))
    



class AveriguacaoListApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    renderer_classes = (ORJSONRenderer,)
    queryset = Averiguacao.objects.none()
    def get(self, request):
        tipo_servico = request.GET.get("tipo_servico")
        last_id = request.GET.get("last_id")
        page_size = int(request.GET.get("page_size", 10))
        result = AveriguacaoListService.executar(
            tipo_servico=tipo_servico,
            last_id=last_id,
            page_size=page_size
        )

        items_dict = []
        for item in result.items:
            items_dict.append({
                "id": item.id,
                "data": str(item.data) if item.data else "",
                "averiguador": item.averiguador or "",
                "pa_da_averiguacao": item.pa_da_averiguacao or "",
                "tipo_servico": item.tipo_servico or "",
                "formulario": item.formulario or {},
                "soltura_id": item.soltura_id or 0,
                "rota_id": item.rota_id or 0,
                "rota": item.rota or "",
                "nao_conformes": item.nao_conformes or 0,
                "inadequados": item.inadequados or 0,
                "detalhes_nao_conformes": item.detalhes_nao_conformes or [],
                "detalhes_inadequados": item.detalhes_inadequados or []
            })
        next_id_cursor = items_dict[-1]["id"] if items_dict else None

        json_bytes = orjson.dumps(
            {
                "items": items_dict,
                "total_itens": result.total_count,
                "next_id_cursor": next_id_cursor
            },
            option=orjson.OPT_PASSTHROUGH_DATACLASS
        )
        return HttpResponse(json_bytes, content_type="application/json", status=200)
    


class AveriguacaoDetailApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    renderer_classes = (ORJSONRenderer,)
    queryset = Averiguacao.objects.none()
    def get(self, request, id: int):
        result_dto = AveriguacaoByIDService.get_by_id(id)
        result_dict = asdict(result_dto)
        json_bytes = orjson.dumps(result_dict, option=orjson.OPT_PASSTHROUGH_DATACLASS)
        return HttpResponse(json_bytes, content_type="application/json", status=200)
    



class AveriguacaoReportApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = (ORJSONRenderer,)
    queryset = Averiguacao.objects.none()
    def get(self, request):
        params = request.GET
        pa_list = params.get("pa", "")
        pa_list = [p.strip() for p in pa_list.split(",")] if pa_list else None
        semana_str = params.get("semana")
        if semana_str:
            try:
                data_inicio = datetime.strptime(semana_str, "%Y-%m-%d").date()
            except ValueError:
                return HttpResponse("Formato de data inválido. Use YYYY-MM-DD.", status=400)
        else:
            hoje = datetime.today().date()
            data_inicio = hoje - timedelta(days=hoje.weekday() + 7)  
        data_fim = data_inicio + timedelta(days=6)
        report_dto = AveriguacaoReportService.gerar_relatorio(
            pa=pa_list,
            data_inicio=data_inicio,
            data_fim=data_fim,
            turno=params.get("turno"),
            servico=params.get("servico", "Remoção"),
            dia_semana=params.get("dia_semana"),
            cursor=params.get("cursor"),
            direction=params.get("direction", "next"),
            limit=int(params.get("limit", 50))
        )
        return HttpResponse(
            orjson.dumps(asdict(report_dto), option=orjson.OPT_PASSTHROUGH_DATACLASS),
            content_type="application/json",
            status=200
        )