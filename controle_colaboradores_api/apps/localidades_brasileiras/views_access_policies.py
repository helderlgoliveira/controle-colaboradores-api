from rest_access_policy import AccessPolicy


class MunicipioAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["*"],
            "effect": "allow"
        }
    ]
