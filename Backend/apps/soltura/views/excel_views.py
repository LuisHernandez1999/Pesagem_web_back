from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.infra.auth.permissions.drf_permissions import DjangoModelPermissionsWithView
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from datetime import datetime
from apps.soltura.models.soltura import Soltura
from apps.soltura.services.excel_services import (
    BaseReportService,
    RemocaoReportService,
    DomiciliarReportService,
    SeletivaReportService,
)
from apps.soltura.documents.excel_generator import BaseReportGenerator


class BaseReportView(GenericAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithView]
    service_class = BaseReportService
    queryset = Soltura.objects.none()

    def get(self, request):
        data_inicio = request.GET.get("data_inicio")
        data_final = request.GET.get("data_final")

        if not data_inicio or not data_final:
            return HttpResponse(
                "Parâmetros data_inicio e data_final são obrigatórios.",
                status=400,
            )

        return self.generate_report(request, data_inicio, data_final)

    def generate_report(self, request, data_inicio, data_final):
        try:
            inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            final_dt = datetime.strptime(data_final, "%Y-%m-%d")
        except ValueError:
            return HttpResponse("Formato de data inválido", status=400)

        service = self.service_class()

        # 🔥 AGORA É ASSIM
        processed_data = service.execute(inicio_dt, final_dt)

        nome_arquivo = (
            f"relatorio_{service.tipo_servico.lower()}_"
            f"{data_inicio}_a_{data_final}.xlsx"
        )

        generator = BaseReportGenerator(
            service=service,
            data_inicio=data_inicio,
            data_final=data_final,
            processed_data=processed_data,
            inicio_dt=inicio_dt,
            final_dt=final_dt,
        )

        caminho = generator.generate(nome_arquivo)

        return FileResponse(
            open(caminho, "rb"),
            as_attachment=True,
            filename=nome_arquivo,
        )


class RemocaoReportView(BaseReportView):
    service_class = RemocaoReportService


class DomiciliarReportView(BaseReportView):
    service_class = DomiciliarReportService


class SeletivaReportView(BaseReportView):
    service_class = SeletivaReportService