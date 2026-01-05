class AuthException(Exception):
    status_code = 400
    default_detail = "Erro de autenticação"

    def __init__(self, detail: str = None):
        # Se passar uma mensagem personalizada, usa ela; senão usa default
        self.detail = detail or self.default_detail
        super().__init__(self.detail)

    def __str__(self):
        return self.detail


class UserAlreadyExists(AuthException):
    status_code = 409
    default_detail = "Usuário já existe"

    def __init__(self, email: str = None):
        if email:
            detail = f"Usuário com email '{email}' já existe"
        else:
            detail = self.default_detail
        super().__init__(detail)


class InvalidCredentials(AuthException):
    status_code = 401
    default_detail = "Credenciais inválidas"


class UserInactive(AuthException):
    status_code = 403
    default_detail = "Usuário inativo"
