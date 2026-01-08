from apps.infra.auth.dto.login_dto import LoginUserDTO
from apps.infra.auth.exceptions.auth_exceptions import InvalidCredentials


def login_user_adapter(request) -> LoginUserDTO:
    data = request.data
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        raise InvalidCredentials("Email e senha são obrigatórios")

    return LoginUserDTO(
        email=email,
        password=password,
    )