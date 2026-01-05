from typing import cast
from django.contrib.auth import authenticate

from apps.infra.Auth.dto.login_dto import LoginUserDTO
from apps.infra.Auth.exceptions.auth_exceptions import (
    InvalidCredentials,
    UserInactive,
)
from apps.infra.Auth.models import CustomUser


class LoginService:
    @staticmethod
    def execute(dto: LoginUserDTO) -> CustomUser:
        user = authenticate(
            email=dto.email,
            password=dto.password,
        )

        if user is None:
            raise InvalidCredentials()

        if not user.is_active:
            raise UserInactive()

        return cast(CustomUser, user)
