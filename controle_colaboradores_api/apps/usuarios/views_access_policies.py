from rest_access_policy import AccessPolicy


class CustomUsuarioAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve",
                       "create", "mudar_grupo",
                       "desativar"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        },
        {
            "action": ["ativar"],
            "principal": ["group:Administradores"],
            "effect": "allow",
            "condition": "esta_ativando_outro_usuario"
        },
        {
            "action": ["retrieve", "mudar_email", "mudar_password"],
            "principal": ["*"],
            "effect": "allow",
            "condition": "is_owner"
        },
        {
            "action": ["mudar_password_apos_reset"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]

    def is_owner(self, request, view, action) -> bool:
        usuario = view.get_object()
        return request.user == usuario

    def esta_ativando_outro_usuario(self, request, view, action) -> bool:
        usuario = view.get_object()
        return request.user != usuario


class GroupAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        }
    ]


class PasswordResetTokenAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            # Admin do Django (não mero usuário do Grupo Administradores):
            "principal": ["admin"],
            "effect": "allow"
        },
        {
            "action": ["create"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]
