class ConfirmacaoServicoError(Exception):
    pass


class ConfirmacaoDuplicadaError(ConfirmacaoServicoError):
    pass


class DadosInvalidosError(ConfirmacaoServicoError):
    pass
