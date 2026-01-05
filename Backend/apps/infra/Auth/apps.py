from django.apps import AppConfig

class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.infra.Auth"
    label = "Auth"

    def ready(self):
        # Força o carregamento completo do pacote models
        from apps.infra.Auth.models.custom_user import CustomUser  # noqa: F401