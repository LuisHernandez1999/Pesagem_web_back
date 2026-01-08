from apps.infra.auth.dto.register_dto import RegisterUserDTO
from apps.infra.auth.exceptions.auth_exceptions import AuthException 
from apps.infra.auth.dto.register_dto import RegisterByInviteDTO

def register_user_adapter(request) -> RegisterUserDTO:
    data = request.data
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        raise AuthException("email e senha são obrigatórios")
    return RegisterUserDTO(
        email=email.strip().lower(),
        password=password,
    )

def register_by_invite_adapter(request) -> RegisterByInviteDTO:
    return RegisterByInviteDTO(
        token=request.data["token"],
        password=request.data["password"],
        email=request.data["email"]
    )

