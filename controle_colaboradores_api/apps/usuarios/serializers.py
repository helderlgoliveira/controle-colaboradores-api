from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import CustomUsuario, PasswordResetToken


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name'
        ]
        read_only_fields = [
            'id',
            'name'
        ]


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['groups'] = GroupSerializer(instance.groups.all()).data
        return data


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = [
            'id',
            'usuario',
            'token'
        ]
        read_only_fields = [
            'id',
            'usuario',
            'token'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['usuario'] = CustomUsuarioSerializer(instance.usuario).data
        return data


class PasswordSerializer(serializers.ModelSerializer):
    nova_senha = serializers.CharField(source="password", required=True)

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'password'
        ]
        read_only_fields = [
            'id'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }