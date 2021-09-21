from rest_framework import serializers
from django.db import transaction
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
    nova_senha = serializers.CharField(required=False)

    class Meta:
        model = CustomUsuario
        fields = [
            'id',
            'email',
            'password',
            'nova_senha'
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

    def validate_password(self, value):
        usuario = getattr(self, 'instance', None)
        if usuario is not None:
            senha_atual_confirmada = usuario.check_password(value)
            if not senha_atual_confirmada:
                raise serializers.ValidationError("Senha incorreta.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        instance = CustomUsuario.objects.create_user(validated_data['email'],
                                                     validated_data['password'])
        groups = validated_data.pop('groups')
        instance.groups.set(groups)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'nova_senha' in validated_data:
            nova_senha = validated_data.pop('nova_senha')
            instance.set_password(nova_senha)

        groups = validated_data.get('groups', instance.groups)
        instance.groups.set(groups)

        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        return instance


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = [
            'id',
            'usuario',
            'token',
            'ativo'
        ]
        read_only_fields = [
            'id',
            'usuario',
            'token'
        ]

    def validate(self, data):
        if "token" in data:
            token_queryset = PasswordResetToken.objects.filter(usuario=data['usuario'], token=data['token'])
            token_existe = token_queryset.exists()
            if not token_existe:
                raise serializers.ValidationError("Token inválido.")
            token = token_queryset.get()
            if not token.ativo:
                raise serializers.ValidationError("Token inativo (já utilizado ou prazo expirou).")
            self.instance = token
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['usuario'] = CustomUsuarioSerializer(instance.usuario).data
        return data

    @transaction.atomic
    def create(self, validated_data):
        instance = PasswordResetToken.objects.create(validated_data['usuario'])
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.ativo = validated_data.get('ativo', instance.ativo)
        instance.save()
        return instance
