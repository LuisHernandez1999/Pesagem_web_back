from django.apps import AppConfig

class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.infra.auth"  
    label = "custom_auth"

    def ready(self):
        from apps.infra.auth.models.custom_user import CustomUser

