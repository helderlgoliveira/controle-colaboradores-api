from rest_access_policy import AccessPolicy


class PerfilAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create", "list", "retrieve", "update", "partial_update"],
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


class DadosParaContatoAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create", "list", "retrieve", "update", "partial_update", "destroy"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        },
        {
            "action": ["create", "list"],
            "principal": ["group:Colaboradores"],
            "effect": "allow",
        },
        {
            "action": ["retrieve", "update", "partial_update", "destroy"],
            "principal": ["group:Colaboradores"],
            "effect": "allow",
            "condition": "is_owner"
        }
    ]

    def is_owner(self, request, view, action) -> bool:
        obj = view.get_object()
        perfil = obj.perfil
        return request.user == perfil.usuario

    @classmethod
    def scope_queryset(cls, request, queryset):
        if request.user.groups.filter(name='Administradores').exists():
            return queryset
        return queryset.filter(perfil=request.user.perfil)


class CargoAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        },
        {
            "action": ["list", "retrieve"],
            "principal": ["group:Colaboradores"],
            "effect": "allow",
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        if request.user.groups.filter(name='Administradores').exists():
            return queryset
        cargos_do_usuario = request.user.perfil.cargos.all(ativo=True)
        return queryset.filter(id__in=cargos_do_usuario).prefetch_related('perfis')


class DepartamentoAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        },
        {
            "action": ["list", "retrieve"],
            "principal": ["group:Colaboradores"],
            "effect": "allow",
        }
    ]

    @classmethod
    def scope_queryset(cls, request, queryset):
        if request.user.groups.filter(name='Administradores').exists():
            return queryset
        departamentos_do_usuario = request.user.perfil.departamentos.filter(ativo=True)
        return queryset.filter(id__in=departamentos_do_usuario).prefetch_related('perfis')

