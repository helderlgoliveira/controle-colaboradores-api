from rest_access_policy import AccessPolicy


class CustomUsuarioAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve", "create", "ativar", "desativar"],
            "principal": ["group:Administradores"],
            "effect": "allow"
        },
        {
            "action": ["retrieve", "mudar_email", "mudar_password"],
            "principal": ["*"],
            "effect": "allow",
            "condition": "is_owner"
        },
        {
            "action": ["criar_nova_password_apos_reset"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]

    def is_owner(self, request, view, action) -> bool:
        usuario = view.get_object()
        return request.user == usuario


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
            "action": ["list"],
            "principal": ["admin"],
            "effect": "allow"
        },
        {
            "action": ["create", "update", "partial_update"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]
