from datetime import  timedelta
from apps.averiguacao.dto.averiguacao_dto import VistoriaDTO,LiderDTO
import json
from typing import List
from apps.averiguacao.models.averiguacao import Averiguacao
from apps.soltura.models.soltura import Soltura
from apps.averiguacao.dto.averiguacao_dto import AveriguacaoItemDTO,MotoristaDTO,AveriguacaoDTO,ColetorDTO
from apps.averiguacao.utils.averiguacao_utils import (
    PA_ESTABELECIDAS,
    METAS_SEMANAIS,
    )
from django.conf import settings


class CriarAveriguacaoMapper:

    @staticmethod
    def dto_para_model(dto):
        return Averiguacao(
            rota_averiguada_id=dto.rota_id,
            tipo_servico=dto.tipo_servico,
            pa_da_averiguacao=dto.pa_da_averiguacao,
            averiguador=dto.averiguador,
            formulario=dto.formulario,
            imagem1=dto.imagem1,
            imagem2=dto.imagem2,
            imagem3=dto.imagem3,
            imagem4=dto.imagem4,
            imagem5=dto.imagem5,
            imagem6=dto.imagem6,
            imagem7=dto.imagem7,
        )
    


class AveriguacaoSemanaMapper:

    @staticmethod
    def to_cards_por_dia(averiguacoes, inicio_semana, fim_semana):
        # Inicializa dias e PA com zero
        dias_da_semana = [(inicio_semana + timedelta(days=i)).isoformat() for i in range((fim_semana - inicio_semana).days + 1)]
        cards_por_dia = {dia: {pa: 0 for pa in PA_ESTABELECIDAS} for dia in dias_da_semana}

        for pa_val, data_val in averiguacoes:
            dia_str = data_val.isoformat()
            if dia_str in cards_por_dia:
                cards_por_dia[dia_str][pa_val] += 1

        return cards_por_dia

    @staticmethod
    def to_meta(cards_por_dia, servico):
        meta_total = METAS_SEMANAIS.get(servico, 0)
        total_realizado = sum(qtd for dia in cards_por_dia.values() for qtd in dia.values())
        total_faltante = max(meta_total - total_realizado, 0)
        perc_realizado = (total_realizado / meta_total * 100) if meta_total > 0 else 0
        perc_faltante = (total_faltante / meta_total * 100) if meta_total > 0 else 0

        return {
            "total": meta_total,
            "realizado": total_realizado,
            "percentual_realizado": round(perc_realizado, 2),
            "faltante": total_faltante,
            "percentual_faltante": round(perc_faltante, 2),
        }
    


class AveriguacaoListMapper:

    @staticmethod
    def dict_to_dto(obj: dict) -> AveriguacaoItemDTO:
        # Garante que formulario é dict
        formulario_raw = obj.get("formulario") or "{}"
        if isinstance(formulario_raw, str):
            try:
                formulario = json.loads(formulario_raw)
            except json.JSONDecodeError:
                formulario = {}
        else:
            formulario = formulario_raw

        # Contagem de não conformes e inadequados
        nao_conformes = sum(1 for v in formulario.values() if str(v).lower() == "não conforme")
        inadequados = sum(1 for v in formulario.values() if str(v).lower() == "inadequado")
        detalhes_nao_conformes = [k for k, v in formulario.items() if str(v).lower() == "não conforme"]
        detalhes_inadequados = [k for k, v in formulario.items() if str(v).lower() == "inadequado"]

        # Define rota (rota ou setor)
        rota = obj.get("rota") or ""

        return AveriguacaoItemDTO(
            id=obj["id"],
            data=obj["data"].isoformat() if hasattr(obj["data"], "isoformat") else obj["data"],
            averiguador=obj.get("averiguador"),
            pa_da_averiguacao=obj.get("pa_da_averiguacao"),
            tipo_servico=obj.get("tipo_servico"),
            formulario=formulario,
            soltura_id=obj.get("soltura_id"),
            rota_id=obj.get("rota_id"),
            rota=rota,
            nao_conformes=nao_conformes,
            inadequados=inadequados,
            detalhes_nao_conformes=detalhes_nao_conformes,
            detalhes_inadequados=detalhes_inadequados
        )

    @staticmethod
    def list_to_dto(objs: list) -> list:
        return [AveriguacaoListMapper.dict_to_dto(obj) for obj in objs]
    

class AveriguacaoByIDMapper:
    @staticmethod
    def model_to_dto(registro_obj) -> AveriguacaoDTO:
        motorista = None
        if registro_obj.rota_averiguada.motorista:
            motorista = MotoristaDTO(
                nome=registro_obj.rota_averiguada.motorista.nome,
                matricula=registro_obj.rota_averiguada.motorista.matricula
            )

        coletores = [
            ColetorDTO(nome=c.nome, matricula=c.matricula)
            for c in registro_obj.rota_averiguada.coletores.all()
        ]

        imagens = [
            f"{settings.R2_PUBLIC_BASE_URL}/{getattr(registro_obj, f'imagem{i}')}"
            for i in range(1, 3)
            if getattr(registro_obj, f"imagem{i}")
        ]

        return AveriguacaoDTO(
            id=registro_obj.id,
            formulario=registro_obj.formulario or {},
            imagens=imagens,
            motorista=motorista,
            coletores=coletores,
            prefixo_veiculo=(
                registro_obj.rota_averiguada.veiculo.prefixo
                if registro_obj.rota_averiguada.veiculo else None
            )
        )

# mappers.py


class AveriguacaoReportMapper:

    @staticmethod
    def to_vistoria_dto(avg: Averiguacao, campos_nao_conformes: list, campos_inadequados: list) -> VistoriaDTO:
        total_campos = len(campos_nao_conformes) + len(campos_inadequados)
        conformidade_servico = ((total_campos - len(campos_nao_conformes)) / total_campos * 100) if total_campos else 100
        qualidade_rota = ((total_campos - len(campos_inadequados)) / total_campos * 100) if total_campos else 100

        return VistoriaDTO(
            vistoria_id=avg.id,
            rota_nome=getattr(avg, "rota_nome", ""),
            pa=avg.pa_da_averiguacao,
            taxas={
                "conformidade_servico": {"percentual": round(conformidade_servico, 2), "campos": campos_nao_conformes},
                "qualidade_rota": {"percentual": round(qualidade_rota, 2), "campos": campos_inadequados}
            }
        )

    @staticmethod
    def to_lider_dto(averiguador: str, total: int, pas: List[str], rotas_setores: List[str], tipos_servico: List[str], turnos: List[str], dias_semana: List[str]) -> LiderDTO:
        return LiderDTO(
            averiguador=averiguador,
            total_averiguacoes=total,
            pas=pas,
            rotas_setores=rotas_setores,
            tipos_servico=tipos_servico,
            turnos=turnos,
            dias_semana=dias_semana
        )