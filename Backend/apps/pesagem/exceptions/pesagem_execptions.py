from rest_framework import status


class PesagemException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Erro relacionado à pesagem"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


# ----------------------------
# Validações de domínio
# ----------------------------

class TipoPesagemInvalida(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Tipo de pesagem inválido"


class VolumeCargaInvalido(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Volume de carga inválido"


class NumeroDocumentoDuplicado(PesagemException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Número do documento já cadastrado"


class PrefixoInvalido(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Prefixo (veículo) inválido"


class CooperativaInvalida(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Cooperativa inválida"


class MotoristaInvalido(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Motorista inválido"


class ColaboradorInvalido(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Colaborador inválido"


# ----------------------------
# Persistência / banco
# ----------------------------

class PesagemCreateError(PesagemException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Erro ao criar pesagem"


class PesagemRelacionamentoError(PesagemException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Erro ao vincular colaboradores à pesagem"


# ----------------------------
# Regras de negócio
# ----------------------------

class HorarioInvalido(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Hora de saída não pode ser menor que a hora de chegada"


class GaragemInvalida(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Garagem inválida"


class TurnoInvalido(PesagemException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Turno inválido"
