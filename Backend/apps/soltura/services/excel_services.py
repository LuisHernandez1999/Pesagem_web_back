from datetime import timedelta
from apps.soltura.models.soltura import Soltura
from apps.soltura.mappers.excel_mappers import SolturaReportProcessMapper

class BaseReportService:
    def __init__(self, tipo_servico, campo_especifico):
        self.tipo_servico = tipo_servico
        self.campo_especifico = campo_especifico

    def fetch_queryset(self, inicio, final):
        final_inclusivo = final + timedelta(days=1)

        return (
            Soltura.objects
            .filter(
                tipo_servico=self.tipo_servico,
                data_soltura__gte=inicio,
                data_soltura__lt=final_inclusivo,
            )
            .select_related("motorista", "veiculo", self.campo_especifico)
            .prefetch_related("coletores")
            .distinct()
        )

    def execute(self, inicio, final):
        qs = self.fetch_queryset(inicio, final)
        return SolturaReportProcessMapper.process(
            qs=qs,
            tipo_servico=self.tipo_servico,
            campo_especifico=self.campo_especifico,
        )



## para criacao de futuros servicos, adicione aqui na service 

class RemocaoReportService(BaseReportService):
    def __init__(self):
        super().__init__("Remoção", "setor")


class DomiciliarReportService(BaseReportService):
    def __init__(self):
        super().__init__("Domiciliar", "rota")


class SeletivaReportService(BaseReportService):
    def __init__(self):
        super().__init__("Seletiva", "rota")
