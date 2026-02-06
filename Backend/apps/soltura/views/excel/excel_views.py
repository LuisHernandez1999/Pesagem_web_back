from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from django.http import JsonResponse
from apps.soltura.models.soltura import Soltura
from apps.soltura.services.excel_services import (
    BaseReportService,
    RemocaoReportService,
    DomiciliarReportService,
    SeletivaReportService,
)
from apps.soltura.tasks.excel_task import gerar_relatorio_excel


class BaseReportView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    service_class = BaseReportService
    queryset = Soltura.objects.none()
    def post(self, request):
        data_inicio = request.GET.get("data_inicio")
        data_final = request.GET.get("data_final")

        if not data_inicio or not data_final:
            return JsonResponse(
                {"erro": "data_inicio e data_final são obrigatórios"},
                status=400,
            )

        task = gerar_relatorio_excel.delay(
            tipo_servico=self.tipo_servico,
            data_inicio=data_inicio,
            data_final=data_final,
        )

        return JsonResponse(
            {
                "task_id": task.id,
                "status": "processando",
            },
            status=202,
        )

class RemocaoReportView(BaseReportView):
    service_class = RemocaoReportService


class DomiciliarReportView(BaseReportView):
    service_class = DomiciliarReportService


class SeletivaReportView(BaseReportView):
    service_class = SeletivaReportService