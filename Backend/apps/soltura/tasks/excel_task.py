from celery import shared_task
from datetime import datetime
from apps.soltura.services.excel_services import (
    RemocaoReportService,
    DomiciliarReportService,
    SeletivaReportService,
)
from apps.soltura.documents.excel_generator import BaseReportGenerator


SERVICE_MAP = {
    "remocao": RemocaoReportService,
    "domiciliar": DomiciliarReportService,
    "seletiva": SeletivaReportService,
}


@shared_task(bind=True)
def gerar_relatorio_excel(
    self,
    tipo_servico: str,
    data_inicio: str,
    data_final: str,
):
    service_class = SERVICE_MAP.get(tipo_servico)

    if not service_class:
        raise ValueError("Tipo de serviço inválido")

    inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
    final_dt = datetime.strptime(data_final, "%Y-%m-%d")

    service = service_class()
    processed_data = service.execute(inicio_dt, final_dt)

    nome_arquivo = (
        f"relatorio_{tipo_servico}_{data_inicio}_a_{data_final}.xlsx"
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

    return {
        "arquivo": nome_arquivo,
        "caminho": caminho,
    }
