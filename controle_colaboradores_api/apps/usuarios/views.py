from django.db import transaction
from django.contrib.auth.models import Group

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_access_policy import AccessViewSetMixin

from .models import CustomUsuario, PasswordResetToken
from .serializers import GroupSerializer, CustomUsuarioSerializer, PasswordResetTokenSerializer
from .views_access_policies import GroupAccessPolicy, CustomUsuarioAccessPolicy, PasswordResetTokenAccessPolicy


class CustomUsuarioViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = CustomUsuarioAccessPolicy
    serializer_class = CustomUsuarioSerializer

    def get_queryset(self):
        return CustomUsuario.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    @transaction.atomic
    @action(detail=True, methods=['patch'])
    def criar_nova_password_apos_reset(self, request, pk=None):
        usuario = self.get_object()
        try:
            token = request.query_params['token']
        except KeyError:
            return Response({'status': 'Token não informado.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomUsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

        token_instance = usuario.password_reset_tokens.get(token=token)
        serializer_token = PasswordResetTokenSerializer(token_instance,
                                                        data={'ativo': False},
                                                        partial=True)
        if serializer_token.is_valid():
            serializer_token.save()
            return Response({'status': 'A nova senha foi registrada.'},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def mudar_password(self, request, pk=None):
        """
        Muda a senha do usuário.
        """
        usuario = self.get_object()
        serializer = CustomUsuarioSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'A nova senha foi registrada.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def mudar_email(self, request, pk=None):
        usuario = self.get_object()

        if 'password' not in request.data:
            return Response({'status': 'Para mudar o e-mail é necessário '
                                       'informar a senha atual.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'O e-mail foi alterado com sucesso.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        usuario = self.get_object()
        serializer = CustomUsuarioSerializer(usuario, data={'is_active': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Usuário ativado.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def desativar(self, request, pk=None):
        usuario = self.get_object()
        serializer = CustomUsuarioSerializer(usuario, data={'is_active': False}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Usuário desativado.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = GroupAccessPolicy
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.all()


class PasswordResetTokenViewSet(AccessViewSetMixin,
                                ModelViewSet):
    access_policy = PasswordResetTokenAccessPolicy
    serializer_class = PasswordResetTokenSerializer

    def get_queryset(self):
        return PasswordResetToken.objects.all()
