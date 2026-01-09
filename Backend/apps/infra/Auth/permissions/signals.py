import logging
from django.conf import settings
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from .roles import ROLES, GIVE_VIEW_ON_OTHER_APPS_TO, SYSTEM_APPS

log = logging.getLogger(__name__)


# =========================
# Usuário → grupo default
# =========================
@receiver(post_save)
def add_default_group_on_user_create(sender, instance, created, **kwargs):
    User = get_user_model()

    if sender is not User or not created or instance.is_superuser:
        return

    group_name = getattr(settings, "DEFAULT_USER_GROUP", "default")
    group, _ = Group.objects.get_or_create(name=group_name)
    instance.groups.add(group)


# =========================
# Helpers de permissão
# =========================
def _permission_codename(op: str, model: str) -> str:
    return f"{op}_{model.lower()}"


def _content_type_for(app_label: str, model_name: str):
    try:
        return ContentType.objects.get(
            app_label=app_label,
            model=model_name.lower(),
        )
    except ContentType.DoesNotExist:
        return None


def _iter_project_content_types():
    return ContentType.objects.exclude(app_label__in=SYSTEM_APPS)


def _grant_perms(group, app_label, model_name, ops):
    ct = _content_type_for(app_label, model_name)
    if not ct:
        log.warning("ContentType não encontrado: %s.%s", app_label, model_name)
        return

    perms = Permission.objects.filter(
        content_type=ct,
        codename__in=[_permission_codename(op, model_name) for op in ops],
    )
    group.permissions.add(*perms)


def _grant_all_perms_for_ct(group, ct):
    perms = Permission.objects.filter(
        content_type=ct,
        codename__regex=r"^(view|add|change|delete)_",
    )
    group.permissions.add(*perms)


def _grant_view_for_other_apps(group):
    others = _iter_project_content_types().exclude(app_label="pesagem")
    perms = Permission.objects.filter(
        content_type__in=others,
        codename__startswith="view_",
    )
    group.permissions.add(*perms)


# =========================
# Aplicação das roles
# =========================
def apply_roles():
    for group_name, rules in ROLES.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        for key, ops in rules.items():
            if key == "*":
                for ct in _iter_project_content_types():
                    _grant_all_perms_for_ct(group, ct)
                continue

            app_label, model_name = key.split(".", 1)
            _grant_perms(group, app_label, model_name, ops)

        if group_name in GIVE_VIEW_ON_OTHER_APPS_TO:
            _grant_view_for_other_apps(group)


# =========================
# post_migrate (ESSENCIAL)
# =========================
@receiver(post_migrate)
def apply_roles_post_migrate(sender, **kwargs):
    try:
        apply_roles()
        print("✅ [roles] Permissões aplicadas")
    except Exception as e:
        print("❌ [roles] Erro:", e)
