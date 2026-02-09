import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from apps.soltura.models.soltura import Soltura
from apps.averiguacao.dto.averiguacao_dto import AveriguacaoCreateRequestDTO
PA_ESTABELECIDAS = ("PA1", "PA2", "PA3", "PA4")

METAS_SEMANAIS = {
    "Remoção": 120,
    "Domiciliar": 100,
    "Seletiva": 90,
}

def calcular_periodo_semana(data_inicio=None, data_fim=None):
    hoje = timezone.localdate()

    if data_inicio and data_fim:
        return (
            datetime.date.fromisoformat(data_inicio),
            datetime.date.fromisoformat(data_fim),
        )

    inicio = hoje - datetime.timedelta(days=hoje.weekday())
    fim = inicio + datetime.timedelta(days=6)
    return inicio, fim




def buscar_soltura(rota_id: int) -> Soltura:
    if not rota_id:
        raise ValueError("Rota é obrigatória")

    return get_object_or_404(Soltura, id=rota_id)


def validar_minimo_imagens(dto: AveriguacaoCreateRequestDTO, minimo: int = 2) -> None:
    imagens = (
        dto.imagem1,
        dto.imagem2,
        dto.imagem3,
        dto.imagem4,
        dto.imagem5,
        dto.imagem6,
        dto.imagem7,
    )

    qtd = sum(1 for img in imagens if img is not None)

    if qtd < minimo:
        raise ValueError(f"É obrigatório enviar pelo menos {minimo} imagens")
    


class AveriguacaoUtils:
    DIAS_MAP = {
        "domingo": 1, "segunda": 2, "terça": 3, "terca": 3,
        "quarta": 4, "quinta": 5, "sexta": 6, "sábado": 7, "sabado": 7
    }

    @staticmethod
    def semana_atual():
        hoje = datetime.date.today()
        inicio = hoje - datetime.timedelta(days=hoje.weekday())
        fim = inicio + datetime.timedelta(days=6)
        return inicio, fim

    @staticmethod
    def format_dia(dia: str | None) -> list[str]:
        if dia:
            chave = dia.strip().lower()
            return [dia.capitalize()] if chave in AveriguacaoUtils.DIAS_MAP else []
        return ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    @staticmethod
    def percentual(total: int, nao_conforme: int) -> float:
        return round(((total - nao_conforme) / total * 100) if total > 0 else 100, 2)