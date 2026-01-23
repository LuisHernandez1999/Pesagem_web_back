from apps.os.models import OrdemServico
from apps.veiculo.models import Veiculo
from apps.os.dto.os_dto import (OrdemServicoCreateDTO, OrdemServicoListDTO,
                                OrdemServicoListFilterDTO,OrdemServicoListResponseDTO)
from apps.os.exceptions.os_exceptions import (
    VeiculoNaoEncontrado,
    OrdemServicoJaAberta
)
from apps.os.models.os import OrdemServico
from apps.os.dto.os_dto import OrdemServicoListItemDTO


class OrdemServicoMapperCreate:
    @staticmethod
    def insert(dto: OrdemServicoCreateDTO) -> int:
        try:
            veiculo = Veiculo.objects.get(prefixo=dto.veiculo_prefixo)
        except Veiculo.DoesNotExist:
            raise VeiculoNaoEncontrado(
                "Veículo não encontrado para o prefixo informado"
            )

        if not dto.conclusao and OrdemServico.objects.filter(
            veiculo=veiculo,
            conclusao__isnull=True
        ).exists():
            raise OrdemServicoJaAberta(
                "Este veículo já possui uma OS em aberto"
            )

        os = OrdemServico.objects.create(
            pa=dto.pa,
            os_numero=dto.os_numero,
            veiculo=veiculo,
            inicio_problema=dto.inicio_problema,
            conclusao=dto.conclusao
        )
        return OrdemServicoListDTO(
            id=os.id,
            pa=os.pa,
            os_numero=os.os_numero,
            veiculo_id=os.veiculo_id,
            veiculo_prefixo=os.veiculo.prefixo,
            inicio_problema=os.inicio_problema.isoformat(),
            conclusao=os.conclusao.isoformat() if os.conclusao else None,
            created_at=os.created_at.isoformat()
        )


class OrdemServicoVisualizacaoMapper:
    @staticmethod
    def listar(queryset) -> list[OrdemServicoListItemDTO]:
        return [
            OrdemServicoListItemDTO(
                id=os.id,
                pa=os.pa,
                os_numero=os.os_numero,
                veiculo_id=os.veiculo_id,
                veiculo_prefixo=os.veiculo.prefixo,
                inicio_problema=os.inicio_problema.isoformat(),
                conclusao=os.conclusao.isoformat() if os.conclusao else None,
                created_at=os.created_at.isoformat()
            )
            for os in queryset
        ]



class OrdemServicoVisualizacaoMapper:

    LIMITE = 20

    @staticmethod
    def listar(dto: OrdemServicoListFilterDTO) -> OrdemServicoListResponseDTO:

        queryset = OrdemServico.objects.select_related("veiculo")

        if dto.veiculo_prefixo:
            queryset = queryset.filter(veiculo__prefixo=dto.veiculo_prefixo)

        if dto.os_numero:
            queryset = queryset.filter(os_numero=dto.os_numero)

        if dto.pa:
            queryset = queryset.filter(pa=dto.pa)

        if dto.aberta is True:
            queryset = queryset.filter(conclusao__isnull=True)

        if dto.aberta is False:
            queryset = queryset.filter(conclusao__isnull=False)

        if dto.cursor_id:
            queryset = queryset.filter(id__lt=dto.cursor_id)

        queryset = queryset.order_by("-id")[: OrdemServicoVisualizacaoMapper.LIMITE + 1]

        registros = list(queryset)

        next_cursor = None
        if len(registros) > OrdemServicoVisualizacaoMapper.LIMITE:
            next_cursor = registros[-1].id
            registros = registros[:-1]

        items = [
            OrdemServicoListItemDTO(
                id=os.id,
                pa=os.pa,
                os_numero=os.os_numero,
                veiculo_id=os.veiculo_id,
                veiculo_prefixo=os.veiculo.prefixo,
                inicio_problema=os.inicio_problema.isoformat(),
                conclusao=os.conclusao.isoformat() if os.conclusao else None,
                created_at=os.created_at.isoformat()
            )
            for os in registros
        ]

        return OrdemServicoListResponseDTO(
            results=items,
            next_cursor=next_cursor,
            limit=OrdemServicoVisualizacaoMapper.LIMITE
        )