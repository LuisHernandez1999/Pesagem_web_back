class ApplicationException(Exception):
    status_code: int = 400
    detail: str = "Erro de aplicação"
    code: str = "application_error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class ColaboradorException(ApplicationException):
    status_code = 400
    code = "colaborador_error"
    detail = "Erro relacionado ao colaborador"


class MatriculaAlreadyExists(ColaboradorException):
    status_code = 409
    code = "matricula_already_exists"
    detail = "Já existe um colaborador com esta matrícula"

class FuncaoInvalida(ColaboradorException):
    status_code = 400
    code = "funcao_invalida"
    detail = "Função inválida. Valores permitidos: MOTORISTA, OPERADOR, COLETOR"

class TurnoInvalido(ColaboradorException):
    status_code = 400
    code = "turno_invalido"
    detail = "Turno inválido. Valores permitidos: DIURNO, NOTURNO, VESPERTINO"

class PaInvalido(ColaboradorException):
    status_code = 400
    code = "pa_invalido"
    detail = "PA inválido. Valores permitidos: PA1, PA2, PA3, PA4"

class ColaboradorNotFound(ColaboradorException):
    status_code = 404
    code = "colaborador_not_found"
    detail = "Colaborador não encontrado"


class FiltroColaboradorInvalido(ColaboradorException):
    status_code = 400
    code = "filtro_colaborador_invalido"
    detail = "Filtro inválido para função e/ou turno"


class StatusInvalido(ColaboradorException):
    status_code = 400
    code = "status_invalido"
    detail = "Status inválido. Valores permitidos: ATIVO, INATIVO"
