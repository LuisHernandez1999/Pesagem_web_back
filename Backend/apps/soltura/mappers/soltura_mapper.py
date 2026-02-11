from collections import defaultdict
from datetime import datetime
from django.db.models import Q, Count,F
from apps.soltura.models import Soltura
from apps.soltura.dto.soltura_dtos import SolturaListItemDTO


class SolturaMapperCreate:
    @staticmethod
    def insert(dto) -> int:
        soltura = Soltura.objects.create(
            tipo_servico=dto.tipo_servico,
            garagem=dto.garagem,
            turno=dto.turno,
            hora_entrega_chave=dto.hora_entrega_chave,
            hora_saida_frota=dto.hora_saida_frota,
            data_soltura=dto.data_soltura,
            status=dto.status,
            veiculo_id=dto.veiculo_id,
            rota_id=dto.rota_id,
            motorista_id=dto.motorista_id,
        )

        if dto.coletores_ids:
            Soltura.coletores.through.objects.bulk_create(
                [
                    Soltura.coletores.through(
                        soltura_id=soltura.id,
                        coletores_id=cid
                    )
                    for cid in dto.coletores_ids
                ],
                batch_size=100
            )

        return soltura.id
    

class SolturaMapperUpdate:
    @staticmethod
    def update(soltura_id, dto) -> int:
        soltura = Soltura.objects.get(id=soltura_id)
        soltura.tipo_servico = dto.tipo_servico
        soltura.garagem = dto.garagem
        soltura.turno = dto.turno
        soltura.hora_entrega_chave = dto.hora_entrega_chave
        soltura.hora_saida_frota = dto.hora_saida_frota
        soltura.data_soltura = dto.data_soltura
        soltura.status = dto.status
        soltura.veiculo_id = dto.veiculo_id
        soltura.rota_id = dto.rota_id
        soltura.motorista_id = dto.motorista_id
        soltura.save()
        if dto.coletores_ids is not None:
            soltura.coletores.clear()
            if dto.coletores_ids:
                Soltura.coletores.through.objects.bulk_create(
                    [
                        Soltura.coletores.through(
                            soltura_id=soltura.id,
                            coletores_id=cid
                        )
                        for cid in dto.coletores_ids
                    ],
                    batch_size=100
                )

        return soltura.id
    
class BaseSolturaListMapper:
    rota_field = False
    setor_field = False

    @classmethod
    def from_model(cls, s):
        return SolturaListItemDTO(
            id=s.id,

            motorista=s.motorista.nome,

            # ✅ MANY TO MANY — lista de nomes
            coletores=[c.nome for c in s.coletores.all()],

            garagem=s.garagem,
            data_soltura=s.data_soltura,

            rota=s.rota.rota if cls.rota_field and s.rota_id else None,
            setor=s.setor.nome_setor if cls.setor_field and s.setor_id else None,

            turno=s.turno,
            status=s.status,
            prefixo=s.veiculo.prefixo,
        )

class RemocaoListMapper(BaseSolturaListMapper):
    setor_field = True


class SeletivaListMapper(BaseSolturaListMapper):
    rota_field = True


class DomiciliarListMapper(SeletivaListMapper):
    pass

class SolturaQuerySetMapper:
    @staticmethod
    def base(tipo_servico):
        return (
            Soltura.objects
            .filter(tipo_servico=tipo_servico)
            .select_related("motorista", "rota", "setor", "veiculo")
            .prefetch_related("coletores")
            .only(
                "id",
                "data_soltura",
                "garagem",
                "turno",
                "status",
                "motorista__nome",
                "veiculo__prefixo",
                "rota__rota",
                "setor__nome_setor",
            )
        )

    @staticmethod
    def aplicar_cursor(qs, cursor):
        if not cursor:
            return qs
        return qs.filter(
            Q(data_soltura__lt=cursor.data_soltura)
            | Q(data_soltura=cursor.data_soltura, id__lt=cursor.id)
        )

    @staticmethod
    def aplicar_busca_global(qs, termo):
        if not termo:
            return qs
        q = Q()
        for palavra in termo.split():
            q |= Q(motorista__nome__icontains=palavra)
            q |= Q(veiculo__prefixo__icontains=palavra)
        return qs.filter(q)

    @staticmethod
    def ordenar(qs):
        return qs.order_by("-data_soltura", "-id")
    
class SolturaAnalyticsQuerySetMapper:
    @staticmethod
    def build(filtros):
        return (
            Soltura.objects
            .filter(filtros)
            .values(
                "status",
                "data_soltura",
                "tipo_servico",
                "turno",
                "garagem",
                "lider",
                "hora_saida_frota",
                "hora_retorno_frota",
                motorista_nome=F("motorista__nome"),
                rota_pa=F("rota__pa"),
                rota_nome=F("rota__rota"),
                rota_tipo_servico=F("rota__tipo_servico"),
                setor_nome=F("setor__nome_setor"),
                setor_regiao=F("setor__regiao"),
            )
            .annotate(total=Count("id"))
        )
class SolturaAnalyticsResultMapper:
    @staticmethod
    def map(qs):
        total_em_andamento = 0
        total_concluido = 0

        por_mes = defaultdict(lambda: {
            "em_andamento": 0,
            "concluido": 0,
            "por_tipo_servico": defaultdict(int),
            "por_turno": defaultdict(int),
            "por_garagem": defaultdict(int),
            "por_motorista": defaultdict(int),
            "por_dia": defaultdict(int)
        })

        curva_por_turno_garagem_lider = defaultdict(lambda: defaultdict(int))

        for r in qs:
            total = r.get("total", 0)
            status = (r.get("status") or "").lower()
            data = r.get("data_soltura")
            tipo_servico = (r.get("tipo_servico") or "").lower()
            turno = (r.get("turno") or "").lower()
            garagem = r.get("garagem") or "Sem Garagem"
            motorista = r.get("motorista_nome") or "Sem Motorista"
            lider = r.get("lider") or "Sem Líder"

            if not data:
                continue

            mes = str(data.month)  # chave sempre string
            dia = str(data.day)    # chave sempre string

            # Status
            if status == "em andamento":
                total_em_andamento += total
                por_mes[mes]["em_andamento"] += total
            elif status == "concluído":
                total_concluido += total
                por_mes[mes]["concluido"] += total

            # Tipo, turno, garagem, motorista
            por_mes[mes]["por_tipo_servico"][str(tipo_servico)] += total
            por_mes[mes]["por_turno"][str(turno)] += total
            por_mes[mes]["por_garagem"][str(garagem)] += total
            por_mes[mes]["por_motorista"][str(motorista)] += total
            por_mes[mes]["por_dia"][dia] += total

            # Curva mês x Turno x Garagem x Líder
            key = f"{turno}-{garagem}-{lider}"  # chave já string
            curva_por_turno_garagem_lider[key][mes] += total

        # Converte defaultdicts internos em dict
        por_mes_final = {}
        mensagens_tendencia = {}
        for mes, metrics in por_mes.items():
            por_mes_final[mes] = {
                "em_andamento": metrics.get("em_andamento", 0),
                "concluido": metrics.get("concluido", 0),
                "por_tipo_servico": dict(metrics.get("por_tipo_servico", {})),
                "por_turno": dict(metrics.get("por_turno", {})),
                "por_garagem": dict(metrics.get("por_garagem", {})),
                "por_motorista": dict(metrics.get("por_motorista", {})),
                "por_dia": dict(metrics.get("por_dia", {})),
            }

            # Tendência diária simples
            dias = sorted(metrics.get("por_dia", {}).keys(), key=int)
            if len(dias) >= 2:
                total_inicio = metrics["por_dia"][dias[0]]
                total_fim = metrics["por_dia"][dias[-1]]
                if total_fim > total_inicio:
                    mensagem = f"No mês {mes}, as saídas estão em crescimento diário."
                elif total_fim < total_inicio:
                    mensagem = f"No mês {mes}, as saídas estão em queda diária."
                else:
                    mensagem = f"No mês {mes}, as saídas estão estáveis."
            else:
                mensagem = f"No mês {mes}, dados insuficientes para análise de tendência diária."
            mensagens_tendencia[mes] = mensagem

        curva_formatada = {str(k): dict(v) for k, v in curva_por_turno_garagem_lider.items()}

        return {
            "total_em_andamento": total_em_andamento,
            "total_concluido": total_concluido,
            "por_mes": por_mes_final,
            "curva_por_turno_garagem_lider": curva_formatada,
            "mensagens_tendencia_diaria": mensagens_tendencia
        }