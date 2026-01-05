# apps/infra/auth/service/register_user.py
from django.db import transaction
from apps.infra.auth.models.custom_user import CustomUser
from apps.infra.auth.dto.register_dto import RegisterUserDTO
from apps.infra.auth.utils.register_utils import email_already_exist

class RegisterUserService:
    @staticmethod
    @transaction.atomic
    def execute(dto: RegisterUserDTO) -> CustomUser:
        # Usa a util para impedir criação de usuário repetido
        email_already_exist(dto.email)

        # Cria usuário
        return CustomUser.objects.create_user(
            email=dto.email,
            password=dto.password,
        )
