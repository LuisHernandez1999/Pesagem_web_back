from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.pesagem.dto.pesagem_dto import (CreatePesagemDTO,PesagemListDTO
                                          ,ExibirPesagemPorMesDTO
                                          ,PesagemCreateDocDTO)
from apps.pesagem.service.pesagem_service import (PesagemServiceCreate
                                                  ,PesagemServiceListTipo, 
                                                  PesagemListService
                                                  ,ExibirPesagemPorMesService )
                                               
from apps.pesagem.exceptions.pesagem_execptions import PesagemException
from apps.pesagem.models.pesagem import Pesagem
from apps.pesagem.tasks.pesagem_task import gerar_relatorio_pesagem_task
from rest_framework import status
from celery.result import AsyncResult


class PesagemCreateApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def post(self, request):
        try:
            dto = CreatePesagemDTO(**request.data)
            pesagem_id = PesagemServiceCreate.create(dto)

            return Response(
                {"pesagem_criada_com_sucesso": pesagem_id},
                status=201
            )
        except PesagemException as e:
            return Response(
                {"detail": e.detail},
                status=e.status_code
            )



class PesagemListApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request):
        dto = PesagemListDTO(
            start_date=request.GET.get("start_date"),
            end_date=request.GET.get("end_date"),
            prefixo=request.GET.get("prefixo"),
            motorista=request.GET.get("motorista"),
            volume_carga=request.GET.get("volume_carga"),
            cooperativa=request.GET.get("cooperativa"),
            numero_doc=request.GET.get("numero_doc"),
            responsavel_coop=request.GET.get("responsavel_coop"),
            tipo_pesagem=request.GET.get("tipo_pesagem"),
            garagem=request.GET.get("garagem"),
            turno=request.GET.get("turno"),
            limit=int(request.GET.get("limit", 20)),
            cursor_id=request.GET.get("cursor"),
        )
        result = PesagemListService.execute(dto)
        return Response(result)

class ExibirPesagemPorMesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request):
        dto = ExibirPesagemPorMesDTO(
            start_date=request.GET.get("start_date"),
            end_date=request.GET.get("end_date"),
            tipo_pesagem=request.GET.get("tipo_pesagem"),
        )
        result = ExibirPesagemPorMesService.execute(dto)
        return Response(result, status=200)

class PesagemTipoServicoView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request):
        try:
            total_seletiva = PesagemServiceListTipo.total_seletiva()
            total_cata_treco = PesagemServiceListTipo.total_cata_treco()
            return Response(
                {
                    "SELETIVA": total_seletiva,
                    "CATA_TRECO": total_cata_treco,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        


class PesagemGerarDocumentoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request):
        dto = PesagemCreateDocDTO(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
            prefixo=request.query_params.get("prefixo"),
            tipo_pesagem=request.query_params.get("tipo_pesagem"),
            volume_carga=request.query_params.get("volume_carga"),
            cooperativa=request.query_params.get("cooperativa"),
            responsavel_coop=request.query_params.get("responsavel_coop"),
            garagem=request.query_params.get("garagem"),
            turno=request.query_params.get("turno"),
        )
        task = gerar_relatorio_pesagem_task.delay(dto.__dict__)

        return Response({
            "message": "Relatório está sendo gerado",
            "task_id": task.id
        }, status=status.HTTP_202_ACCEPTED)


class PesagemRelatorioStatusAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    queryset = Pesagem.objects.none()
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)

        if task_result.status == 'SUCCESS':
            return Response({
                "status": task_result.status,
                "file_path": task_result.result
            })
        else:
            return Response({
                "status": task_result.status
            })