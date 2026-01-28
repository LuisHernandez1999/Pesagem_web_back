from apps.confirmacao.exceptions.exceptions_confirmacao import DadosInvalidosError


def validar_confirmacao(dto):
    if not dto.data_servico:
        raise DadosInvalidosError("data_servico é obrigatória")

    if not dto.tipo_servico:
        raise DadosInvalidosError("tipo_servico é obrigatório")

    if not dto.imagens:
        raise DadosInvalidosError("É necessário ao menos uma imagem")
