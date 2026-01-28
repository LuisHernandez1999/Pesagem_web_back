from apps.confirmacao.models.confirmacao import ConfirmacaoServico, ImagemConfirmacao
from apps.confirmacao.utils.encoder_utils import gerar_tag_doc
from apps.confirmacao.dto.confirmacao_dto import ConfirmacaoServicoDTO


class ConfirmacaoCreateMapper:

    @staticmethod
    def criar(dto) -> ConfirmacaoServicoDTO:
        confirmacao = ConfirmacaoServico.objects.create(
            tag_doc=gerar_tag_doc(),
            nome_vistoriador=dto.nome_vistoriador,
            data_servico=dto.data_servico,
            tipo_servico=dto.tipo_servico,
        )

        imagens = [
            ImagemConfirmacao(
                confirmacao=confirmacao,
                imagem=img.imagem,
                latitude=img.latitude,
                longitude=img.longitude,
            )
            for img in dto.imagens
        ]

        ImagemConfirmacao.objects.bulk_create(imagens)

        imagens_dto = [
            {
                "imagem": img.imagem,
                "latitude": img.latitude,
                "longitude": img.longitude,
            }
            for img in imagens
        ]

        return ConfirmacaoServicoDTO(
            id=confirmacao.id,
            tag_doc=confirmacao.tag_doc,
            nome_vistoriador=confirmacao.nome_vistoriador,
            data_servico=confirmacao.data_servico,
            tipo_servico=confirmacao.tipo_servico,
            imagens=imagens_dto,
        )
