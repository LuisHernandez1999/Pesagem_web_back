from django.db import IntegrityError, transaction
from django.db import transaction
from apps.infra.auth.models.custom_user import CustomUser
from apps.infra.auth.exceptions.auth_exceptions import UserAlreadyExists
from apps.infra.auth.dto.register_dto import RegisterUserDTO


class RegisterUserService:
    @staticmethod
    @transaction.atomic
    def execute(dto: RegisterUserDTO) -> CustomUser:
        try:
            return CustomUser.objects.create_user(
                email=dto.email,
                password=dto.password,
            )
        except IntegrityError:
            raise UserAlreadyExists()