from django.core.exceptions import ValidationError

class DomainException(ValidationError):

    def __init__(self, message: str):
        super().__init__(message)


class OrdemServicoNaoEncontrada(DomainException):
    def __init__(self):
        super().__init__("Ordem de Serviço não encontrada para o número informado")


class ColaboradorNaoEncontrado(DomainException):
    def __init__(self):
        super().__init__("Colaborador não encontrado pela matrícula")


class StatusMovimentacaoInvalido(DomainException):
    def __init__(self, status: str):
        super().__init__(f"Status inválido: {status}")


class DataHoraInvalida(DomainException):
    def __init__(self):
        super().__init__("data_hora inválida ou obrigatória")


class CampoObrigatorio(DomainException):
    def __init__(self, campo: str):
        super().__init__(f"{campo} é obrigatório")
