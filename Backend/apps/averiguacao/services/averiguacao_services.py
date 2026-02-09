from apps.averiguacao.mappers.averiguacao_mapper import (CriarAveriguacaoMapper,
                                                         AveriguacaoSemanaMapper,
                                                         AveriguacaoListMapper,
                                                         AveriguacaoByIDMapper,
                                                         AveriguacaoReportMapper)
from apps.averiguacao.dto.averiguacao_dto import(AveriguacaoCreateRequestDTO,
                                                AveriguacaoCreateResponseDTO,
                                                AveriguacaoListResponseDTO,
                                                AveriguacaoResponseDTO,
                                               )
from django.db import transaction,connection
from apps.averiguacao.models.averiguacao import Averiguacao
from datetime import  timedelta,timezone
from django.db.models import Q
from django.utils import timezone
import json
from apps.averiguacao.query.averiguacao_queries import AveriguacaoQuery
from apps.averiguacao.mappers.averiguacao_mapper import AveriguacaoReportMapper
from apps.averiguacao.dto.averiguacao_dto import  ReportAveriguacaoDTO



TIPOS_SERVICO = ['Seletiva', 'Remoção', 'Domiciliar']

class CriarAveriguacaoService:

    @transaction.atomic
    @staticmethod
    def executar(dto: AveriguacaoCreateRequestDTO) -> AveriguacaoCreateResponseDTO:
        averiguacao = CriarAveriguacaoMapper.dto_para_model(dto)
        averiguacao.full_clean()
        averiguacao.save()

        return AveriguacaoCreateResponseDTO(
            id=averiguacao.id,
            mensagem="Averiguação criada com sucesso"
        )


class AveriguacaoSemanaService:

    @staticmethod
    def execute(pa=None, turno=None, servico=None, dia_semana=None):
        hoje = timezone.localdate() 
        servico = servico or "Remoção"

        if dia_semana:
            inicio_semana = dia_semana["inicio"]
            fim_semana = dia_semana["fim"]
        else:
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            fim_semana = inicio_semana + timedelta(days=6)
        filtro = Q(tipo_servico=servico, data__range=(inicio_semana, fim_semana))
        if pa:
            filtro &= Q(pa_da_averiguacao=pa)
        if turno:
            filtro &= Q(rota_averiguada__turno=turno)
        averiguacoes = Averiguacao.objects.filter(filtro).values_list("pa_da_averiguacao", "data")
        cards_por_dia = AveriguacaoSemanaMapper.to_cards_por_dia(averiguacoes, inicio_semana, fim_semana)
        meta = AveriguacaoSemanaMapper.to_meta(cards_por_dia, servico)
        return {
            "servico": servico,
            "turno": turno,
            "pa": pa,
            "cards_por_dia": cards_por_dia,
            "periodo_inicio": inicio_semana.isoformat(),
            "periodo_fim": fim_semana.isoformat(),
            "meta": meta,
        }
    @staticmethod
    def get_averiguacao_service(*args, **kwargs):
        return AveriguacaoSemanaService.execute(*args, **kwargs)
    


class AveriguacaoListService:
    @staticmethod
    def executar(tipo_servico=None, last_id=None, page_size=10) -> AveriguacaoListResponseDTO:
        params = []
        where = ""
        if last_id:
            where = "WHERE a.id < %s"
            params.append(last_id)
        if tipo_servico:
            where += " AND a.tipo_servico = %s" if where else "WHERE a.tipo_servico = %s"
            params.append(tipo_servico)

        params.append(page_size)

        query = f"""
            SELECT a.id, a.data, a.averiguador, a.pa_da_averiguacao, a.tipo_servico,
                   a.formulario, s.id AS soltura_id, r.id AS rota_id,
                   COALESCE(r.rota, st.nome_setor) AS rota
            FROM averiguacao a
            LEFT JOIN soltura s ON a.rota_averiguada_id = s.id
            LEFT JOIN rota r ON s.rota_id = r.id
            LEFT JOIN setor st ON s.setor_id = st.id
            {where}
            ORDER BY a.id DESC
            LIMIT %s;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        dto_list = AveriguacaoListMapper.list_to_dto(rows)
        total_count = len(dto_list) if not last_id else len(dto_list)
        return AveriguacaoListResponseDTO(items=dto_list, total_count=total_count)
    


class AveriguacaoByIDService:
    @staticmethod
    def get_by_id(id: int) -> AveriguacaoResponseDTO:
        try:
            registro_obj = Averiguacao.objects.select_related(
                "rota_averiguada__motorista",
                "rota_averiguada__veiculo"
            ).prefetch_related(
                "rota_averiguada__coletores"
            ).filter(
                id=id,
                tipo_servico__in=TIPOS_SERVICO
            ).first()

            if not registro_obj:
                return AveriguacaoResponseDTO(
                    success=False,
                    data=[],
                    message=f"Nenhuma averiguação encontrada para id={id}."
                )

            dto = AveriguacaoByIDMapper.model_to_dto(registro_obj)
            return AveriguacaoResponseDTO(success=True, data=[dto])

        except Exception as e:
            return AveriguacaoResponseDTO(
                success=False,
                data=[],
                message="Erro ao buscar averiguação.",
                error=str(e)
            )
        

class AveriguacaoReportService:
    @staticmethod
    def gerar_relatorio(pa=None, data_inicio=None, data_fim=None, turno=None, servico="Remoção", dia_semana=None, cursor=None, direction="next", limit=50) -> ReportAveriguacaoDTO:

        registros, total = AveriguacaoQuery.buscar_averiguacoes(
            pa=pa,
            turno=turno,
            servico=servico,
            dia_semana=dia_semana,
            cursor=cursor,
            direction=direction,
            limit=limit,
            data_inicio=data_inicio,
            data_fim=data_fim
        )


        vistorias = []
        registros_com_problema = 0
        for avg in registros[:limit]:
            campos_nao_conformes = []
            campos_inadequados = []

            if avg.formulario:
                try:
                    formulario = json.loads(avg.formulario)
                except:
                    formulario = {}
                for campo, valor in formulario.items():
                    val_lower = str(valor).lower()
                    if val_lower == "não conforme":
                        campos_nao_conformes.append(campo)
                    elif val_lower == "inadequado":
                        campos_inadequados.append(campo)

            if campos_nao_conformes or campos_inadequados:
                registros_com_problema += 1
            vistorias.append(AveriguacaoReportMapper.to_vistoria_dto(avg, campos_nao_conformes, campos_inadequados))
        taxa_geral = ((total - registros_com_problema) / total * 100) if total else 0
        lideres_dict = {}
        for avg in registros[:limit]:
            key = avg.averiguador
            if key not in lideres_dict:
                lideres_dict[key] = {
                    "total": 0,
                    "pas": set(),
                    "rotas_setores": set(),
                    "tipos_servico": set(),
                    "turnos": set()
                }
            lideres_dict[key]["total"] += 1
            lideres_dict[key]["pas"].add(avg.pa_da_averiguacao)
            lideres_dict[key]["rotas_setores"].add(getattr(avg, "rota_nome", ""))
            lideres_dict[key]["tipos_servico"].add(avg.tipo_servico)
            lideres_dict[key]["turnos"].add(getattr(avg.rota_averiguada, "turno", ""))

        lideres = [
            AveriguacaoReportMapper.to_lider_dto(
                averiguador=k,
                total=v["total"],
                pas=list(v["pas"]),
                rotas_setores=list(v["rotas_setores"]),
                tipos_servico=list(v["tipos_servico"]),
                turnos=list(v["turnos"]),
                dias_semana=[dia_semana.capitalize()] if dia_semana else ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            )
            for k, v in lideres_dict.items()
        ]
        next_cursor = registros[-1].id if registros else None
        prev_cursor = registros[0].id if registros else None
        return ReportAveriguacaoDTO(
            periodo="semana_atual",
            pa=pa,
            turno=turno,
            servico=servico,
            dias_semana=[dia_semana.capitalize()] if dia_semana else ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
            total_respostas=total,
            conformidade_servico={
                "percentual": round(taxa_geral, 2),
                "total_formularios_com_irregularidades": registros_com_problema,
                "total_avg": total
            },
            total_nao_conformes=registros_com_problema,
            vistorias=vistorias,
            lideres=lideres,
            next_cursor=next_cursor,
            previous_cursor=prev_cursor
        )