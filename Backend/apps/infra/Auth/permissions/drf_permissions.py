from rest_framework.permissions import DjangoModelPermissions, BasePermission

class DjangoModelPermissionsWithView(DjangoModelPermissions):
    """
    Igual ao DjangoModelPermissions, mas exige 'view_*' nos GETs.
    """
    perms_map = {
        "GET":    ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [], "HEAD": [],
        "POST":   ["%(app_label)s.add_%(model_name)s"],
        "PUT":    ["%(app_label)s.change_%(model_name)s"],
        "PATCH":  ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
    def has_permission(self, request, view):
        has = super().has_permission(request, view)
        if not has:
            # Monte a lista de permissões exigidas para esta ação
            model = getattr(getattr(view, "queryset", None), "model", None)
            if model:
                app_label = model._meta.app_label
                model_name = model._meta.model_name
                required = [p % {"app_label": app_label, "model_name": model_name}
                            for p in self.perms_map.get(request.method, [])]
                # DRF usa `permission.message` no 403
                self.message = f"Você não tem permissão para esta ação. Requer: {', '.join(required)}"
        return has

def role_required(*group_names: str):
    """
    Permissão simples por grupo (para endpoints que não mapeiam 1:1 para um Model).
    Uso:
      permission_classes = [IsAuthenticated, role_required("sac","torre")]    """
    class _RolePermission(BasePermission):
        def has_permission(self, request, view):
            u = request.user
            return bool(u and u.is_authenticated and u.groups.filter(name__in=group_names).exists())
    return _RolePermission
