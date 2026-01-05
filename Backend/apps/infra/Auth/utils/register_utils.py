from apps.infra.auth.models.custom_user import CustomUser
from apps.infra.auth.exceptions.auth_exceptions import UserAlreadyExists

def email_already_exist(email: str):
    if CustomUser.objects.filter(email=email).exists():
        raise UserAlreadyExists(email)
    