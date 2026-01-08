# apps/infra/auth/service/register_user.py
from django.db import transaction
from apps.infra.auth.models.custom_user import CustomUser
from apps.infra.auth.dto.register_dto import RegisterUserDTO
from apps.infra.auth.utils.register_utils import email_already_exist
from django.shortcuts import get_object_or_404
from apps.infra.auth.dto.register_dto import RegisterByInviteDTO
from apps.infra.auth.models.user_invite import UserInvite
from apps.infra.auth.models.custom_user import CustomUser
from apps.infra.auth.utils.register_utils import ensure_user_does_not_exist
from apps.infra.auth.exceptions.auth_exceptions import AuthException
#registro tradicionarl
class RegisterUserService:
    @staticmethod
    @transaction.atomic
    def execute(dto: RegisterUserDTO) -> CustomUser:
        email_already_exist(dto.email)
        return CustomUser.objects.create_user(
            email=dto.email,
            password=dto.password,
        )
#### registro por convite
class RegisterUserByInviteService:
    @staticmethod
    @transaction.atomic
    def execute(dto: RegisterByInviteDTO) -> CustomUser:
        invite = get_object_or_404(UserInvite, token=dto.token)

        if not invite.is_valid():
            raise AuthException("Convite inválido ou expirado")

        # 🔥 valida se o email bate com o convite
        if invite.email.strip().lower() != dto.email:
            raise AuthException("Email não corresponde ao convite")

        ensure_user_does_not_exist(dto.email)

        user = CustomUser.objects.create_user(
            email=dto.email,
            password=dto.password,
        )

        invite.used = True
        invite.save(update_fields=["used"])

        return user