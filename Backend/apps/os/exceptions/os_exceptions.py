from django.core.exceptions import ValidationError


class OrdemServicoException(ValidationError):
    pass


class PaObrigatorio(OrdemServicoException):
    pass


class OsNumeroObrigatorio(OrdemServicoException):
    pass


class VeiculoPrefixoObrigatorio(OrdemServicoException):
    pass


class VeiculoNaoEncontrado(OrdemServicoException):
    pass


class InicioProblemaInvalido(OrdemServicoException):
    pass


class ConclusaoInvalida(OrdemServicoException):
    pass


class OrdemServicoJaAberta(OrdemServicoException):
    pass
