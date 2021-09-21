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
        usuario = CustomUsuario.objects.create_user(validated_data['email'],
                                          validated_data['password'])
        groups = validated_data.pop('groups')
        for group in groups:
            usuario.groups.add(group)
        return usuario

    @transaction.atomic
    def update(self, instance, validated_data):
        # TODO continuar daqui:
        #  pop nova_senha para set_password, e restante
        #  dar update **validated data ver algumn exemplo nas docs
        instance.set_password(validated_data.get('nova_senha'))
        # TODO PasswordResetTokenSerializer
        instance.save()
        return instance


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
