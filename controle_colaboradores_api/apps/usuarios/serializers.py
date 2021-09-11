from rest_framework import serializers

from .models import CustomUsuario


class CustomUsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'email',
            'password',
            'groups',
            'last_login',
            'is_active'
        ]
        read_only_fields = [
            'id',
            'last_login'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
