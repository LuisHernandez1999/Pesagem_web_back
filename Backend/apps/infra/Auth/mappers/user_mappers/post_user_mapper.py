from apps.infra.auth.dto.register_dto import RegisterUserDTO

def register_user_mapper(request) -> RegisterUserDTO:
    return RegisterUserDTO(
        email=request.data["email"],
        password=request.data["password"],
    )