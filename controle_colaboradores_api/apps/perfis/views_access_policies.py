from rest_access_policy import AccessPolicy


class PerfilAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "create", "retrieve", "update", "partial_update"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        },
        {
            "action": ["retrieve", "update", "partial_update"],
            "principal": ["group:Colaboradores"],
            "effect": "allow",
            "condition": "is_owner"
        }
    ]

    def is_owner(self, request, view, action) -> bool:
        perfil = view.get_object()
        return request.user == perfil.usuario

    @classmethod
    def scope_queryset(cls, request, queryset):
        if request.user.groups.filter(name='Administradores').exists():
            return queryset
        return queryset.filter(status='Colaboradores')

