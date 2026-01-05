class AuthException(Exception):
    status_code = 400
    default_detail = "Erro de autenticação"


class UserAlreadyExists(AuthException):
    status_code = 409
    default_detail = "Usuário já existe"


class InvalidCredentials(AuthException):
    status_code = 401
    default_detail = "Credenciais inválidas"


class UserInactive(AuthException):
    status_code = 403
    default_detail = "Usuário inativo"
