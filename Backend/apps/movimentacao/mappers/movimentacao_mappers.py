from apps.movimentacao.models import Movimentacao
from apps.os.models import OrdemServico
from apps.colaborador.models import Colaborador
from apps.movimentacao.dto.movimentacao_dto  import MovimentacaoCreateDTO,MovimentacaoListCursorDTO,MovimentacaoListDTO
from apps.movimentacao.exceptions.movimentacao_exceptions import (
    OrdemServicoNaoEncontrada,
    ColaboradorNaoEncontrado,
)
from typing import List, Optional, Tuple
###### SERVICE CREATE
class MovimentacaoMapperCreate:
    @staticmethod
    def insert(dto: MovimentacaoCreateDTO) -> Movimentacao:

        os = (
            OrdemServico.objects
            .filter(os_numero=dto.os_numero)
            .order_by("-id")
            .first()
        )

        if not os:
            raise OrdemServicoNaoEncontrada()

        try:
            responsavel = Colaborador.objects.get(
                matricula=dto.responsavel_matricula
            )
        except Colaborador.DoesNotExist:
            raise ColaboradorNaoEncontrado()

        return Movimentacao.objects.create(
            os=os,
            data_hora=dto.data_hora,
            status=dto.status,
            responsavel=responsavel,
            observacao=dto.observacao
        )
    
###### SERVICE LISTAGEM COM FILTROS
class MovimentacaoMapperList:
    @staticmethod
    def listar_com_cursor(
        dto: MovimentacaoListCursorDTO
    ) -> Tuple[List[MovimentacaoListDTO], Optional[int]]:

        qs = (
            Movimentacao.objects
            .select_related("os", "os__veiculo", "responsavel")
            .order_by("-id_movimentacao")
        )

        # =========================
        # FILTROS MOVIMENTACAO
        # =========================
        if dto.status:
            qs = qs.filter(status=dto.status)

        if dto.observacao:
            qs = qs.filter(observacao__icontains=dto.observacao)

        # =========================
        # FILTROS DATA
        # =========================
        if dto.data:
            qs = qs.filter(data_hora__date=dto.data)

        if dto.data_inicio:
            qs = qs.filter(data_hora__date__gte=dto.data_inicio)

        if dto.data_fim:
            qs = qs.filter(data_hora__date__lte=dto.data_fim)

        # =========================
        # FILTROS RESPONSAVEL
        # =========================
        if dto.responsavel_matricula:
            qs = qs.filter(
                responsavel__matricula=dto.responsavel_matricula
            )

        if dto.responsavel_nome:
            qs = qs.filter(
                responsavel__nome__icontains=dto.responsavel_nome
            )

        # =========================
        # FILTROS OS
        # =========================
        if dto.os_id:
            qs = qs.filter(os_id=dto.os_id)

        if dto.os_numero:
            qs = qs.filter(os__os_numero__icontains=dto.os_numero)

        if dto.pa:
            qs = qs.filter(os__pa=dto.pa)

        if dto.veiculo_prefixo:
            qs = qs.filter(
                os__veiculo__prefixo=dto.veiculo_prefixo
            )

        # =========================
        # CURSOR
        # =========================
        if dto.next_cursor:
            qs = qs.filter(id_movimentacao__lt=dto.next_cursor)
        # =========================
        # PAGINAÇÃO
        # =========================
        itens = list(qs[: dto.limit + 1])
        has_next = len(itens) > dto.limit
        itens = itens[: dto.limit]

        next_cursor = (
            itens[-1].id_movimentacao if has_next else None
        )

        dto_list = [
            MovimentacaoListDTO(
                id=m.id_movimentacao,
                os_id=m.os_id,
                os_numero=m.os.os_numero,
                pa=m.os.pa,
                veiculo_prefixo=m.os.veiculo.prefixo,
                data_hora=m.data_hora.isoformat(),
                status=m.status,
                responsavel_matricula=m.responsavel.matricula,
                responsavel_nome=m.responsavel.nome,
                observacao=m.observacao,
            )
            for m in itens
        ]

        return dto_list, next_cursor