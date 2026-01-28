from datetime import timedelta
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.infra.auth.exceptions.auth_exceptions import InvalidCredentials


class RefreshTokenService:
    REFRESH_RENEW_THRESHOLD = timedelta(days=1) 
    @staticmethod
    def execute(dto) -> dict:
        try:
            refresh = RefreshToken(dto.refresh)
        except TokenError:
            raise InvalidCredentials("Refresh token inválido")

        exp_timestamp = refresh["exp"]
        expires_at = now().fromtimestamp(exp_timestamp)

        remaining_time = expires_at - now()
        access_token = refresh.access_token

        response = {
            "access": str(access_token),
        }
        if remaining_time <= RefreshTokenService.REFRESH_RENEW_THRESHOLD:
            refresh.set_jti()
            refresh.set_exp()
            response["refresh"] = str(refresh)

        return response
