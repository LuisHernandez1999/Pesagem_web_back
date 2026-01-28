from collections import defaultdict
from apps.soltura.dto.remocao_dto import SolturaResumoDTO, SolturaCreateDTO,SolturaListItemDTO
from apps.soltura.models.soltura import Soltura
from apps.celular.models.celular import Celular
from apps.veiculo.models.veiculo import Veiculo
from apps.colaborador.models.colaborador import Colaborador
from apps.soltura.models.rota import Rota
from apps.soltura.models.setor import Setor
from django.db.models import Q


class SolturaRemocaoMapper:
    @staticmethod
    def from_queryset(qs) -> SolturaResumoDTO:
        total_em_andamento = 0
        total_concluido = 0
        contagem_dia_semana = defaultdict(int)
        contagem_mes = defaultdict(int)
        contagem_dia = defaultdict(int)
        for row in qs:
            status = (row["status"] or "").lower()
            total = row["total"]
            data = row["data_soltura"]
            if status == "em andamento":
                total_em_andamento += total
            elif status == "concluído":
                total_concluido += total
            if data:
                contagem_dia_semana[data.isoweekday()] += total
                contagem_mes[data.month] += total
                contagem_dia[data.strftime("%Y-%m-%d")] += total

        return SolturaResumoDTO(
            total_em_andamento=total_em_andamento,
            total_concluido=total_concluido,
            contagem_dia_semana=dict(contagem_dia_semana),
            contagem_mes=dict(contagem_mes),
            contagem_dia=dict(contagem_dia),
            mes_mais_saida=max(contagem_mes, key=contagem_mes.get) if contagem_mes else None,
        )
    

class RemocaoQuerySetMapper:
    @staticmethod
    def base_queryset():
        return (
            Soltura.objects
            .filter(tipo_servico="Remoção")
            .select_related("motorista", "setor", "veiculo")
            .prefetch_related("coletores")
            .only(
                "id", "data_soltura", "garagem", "turno", "status",
                "motorista__nome", "setor__nome_setor", "veiculo__prefixo"
            )
        )
    @staticmethod
    def aplicar_cursor(qs, cursor):
        if not cursor:
            return qs

        return qs.filter(
            Q(data_soltura__lt=cursor.data_soltura) |
            Q(data_soltura=cursor.data_soltura, id__lt=cursor.id)
        )

    @staticmethod
    def aplicar_filtros(qs, filters):
        if not filters:
            return qs

        filters = {
            ('veiculo__prefixo' if k == 'prefixo' else k): v
            for k, v in filters.items()
        }
        return qs.filter(**filters)

    @staticmethod
    def aplicar_date_range(qs, start, end):
        if start and end:
            return qs.filter(data_soltura__range=[start, end])
        if start:
            return qs.filter(data_soltura__gte=start)
        if end:
            return qs.filter(data_soltura__lte=end)
        return qs

    @staticmethod
    def aplicar_search(qs, search):
        if not search:
            return qs

        q = Q()
        for field, value in search.items():
            if value:
                field = 'veiculo__prefixo' if field == 'prefixo' else field
                q |= Q(**{f"{field}__icontains": value})
        return qs.filter(q)

    @staticmethod
    def aplicar_busca_global(qs, termo):
        if not termo:
            return qs

        q = Q()
        for palavra in termo.split():
            q |= (
                Q(motorista__nome__icontains=palavra) |
                Q(setor__nome_setor__icontains=palavra) |
                Q(veiculo__prefixo__icontains=palavra)
            )
        return qs.filter(q)

    @staticmethod
    def ordenar(qs):
        return qs.order_by("-data_soltura", "-id")
    @staticmethod
    def paginar(qs, limit):
        return qs[:limit]
    

class RemocaoListMapper:
    @staticmethod
    def from_model(s):
        return SolturaListItemDTO(
            id=s.id,
            motorista=s.motorista.nome if s.motorista else None,
            coletores=[c.nome for c in s.coletores.all()],
            garagem=s.garagem,
            data_soltura=s.data_soltura,
            setor=s.setor.nome_setor if s.setor else None,
            turno=s.turno,
            status=s.status,
            prefixo=s.veiculo.prefixo if s.veiculo else None,
        )



class SolturaCreateMapper:
    @staticmethod
    def from_dto(dto: SolturaCreateDTO) -> Soltura:
        motorista = Colaborador.objects.get(id=dto.motorista_id)
        veiculo = Veiculo.objects.get(id=dto.veiculo_id)
        rota = Rota.objects.get(id=dto.rota_id) if dto.rota_id else None
        setor = Setor.objects.get(id=dto.setor_id) if dto.setor_id else None
        celular = Celular.objects.get(id=dto.celular_id) if dto.celular_id else None
        soltura = Soltura(
            motorista=motorista,
            veiculo=veiculo,
            hora_entrega_chave=dto.hora_entrega_chave,
            hora_saida_frota=dto.hora_saida_frota,
            data_soltura=dto.data_soltura,
            garagem=dto.garagem,
            lider=dto.lider,
            tipo_servico=dto.tipo_servico,
            turno=dto.turno,
            rota=rota,
            setor=setor,
            celular_id=celular,
            celular=dto.celular
        )
        return soltura