from django.db import transaction
from django.contrib.auth.models import Group

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_access_policy import AccessViewSetMixin

from .models import CustomUsuario, PasswordResetToken
from .serializers import (
    GroupSerializer,
    CustomUsuarioSerializer,
    CustomUsuarioMudarPasswordSerializer,
    CustomUsuarioMudarPasswordAposResetSerializer,
    CustomUsuarioMudarEmailSerializer,
    CustomUsuarioMudarGrupoSerializer,
    CustomUsuarioMudarAtivacaoSerializer,
    PasswordResetTokenSerializer
)
from .views_access_policies import GroupAccessPolicy, CustomUsuarioAccessPolicy, PasswordResetTokenAccessPolicy


class CustomUsuarioViewSet(AccessViewSetMixin,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    access_policy = CustomUsuarioAccessPolicy
    serializer_class = CustomUsuarioSerializer

    def get_queryset(self):
        return CustomUsuario.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    @transaction.atomic
    @action(detail=True, methods=['patch'], serializer_class=CustomUsuarioMudarPasswordAposResetSerializer)
    def mudar_password_apos_reset(self, request, pk=None):
        """
        Mudar a password do usuário após a solicitação de resetá-la.
        Consequentemente, é desativado o token que permitiu a alteração.
        """
        usuario = self.get_object()
        try:
            token = request.query_params['token']
        except KeyError:
            return Response({'status': 'Token não informado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            token_instance = usuario.password_reset_tokens.get(token=token,
                                                               ativo=True)
        except PasswordResetToken.DoesNotExist:
            return Response({'status': 'Token inexistente.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer_token = PasswordResetTokenSerializer(token_instance,
                                                        data={'ativo': False},
                                                        partial=True)
        if serializer_token.is_valid():
            serializer_token.save()
        else:
            return Response(serializer_token.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer_usuario = self.get_serializer(
            usuario,
            data=request.data,
            partial=True
        )

        if serializer_usuario.is_valid():
            serializer_usuario.save()
            return Response({'status': 'A nova senha foi registrada.'},
                            status=status.HTTP_200_OK)
        return Response(serializer_usuario.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=CustomUsuarioMudarPasswordSerializer)
    def mudar_password(self, request, pk=None):
        """
        Muda a senha do usuário.
        """
        usuario = self.get_object()
        serializer = self.get_serializer(usuario,
                                         data=request.data,
                                         partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'A nova senha foi registrada.'},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=CustomUsuarioMudarEmailSerializer)
    def mudar_email(self, request, pk=None):
        usuario = self.get_object()

        if 'password' not in request.data:
            return Response({'status': 'Para mudar o e-mail é necessário '
                                       'informar a senha atual.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'O e-mail foi alterado com sucesso.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=CustomUsuarioMudarGrupoSerializer)
    def mudar_grupo(self, request, pk=None):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'O grupo foi alterado com sucesso.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=CustomUsuarioMudarAtivacaoSerializer)
    def ativar(self, request, pk=None):
        usuario = self.get_object()
        serializer = self.get_serializer(
            usuario,
            data={'is_active': True},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Usuário ativado.'},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=CustomUsuarioMudarAtivacaoSerializer)
    def desativar(self, request, pk=None):
        usuario = self.get_object()
        serializer = self.get_serializer(
            usuario,
            data={'is_active': False},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Usuário desativado.'},
                            status=status.HTTP_200_OK)

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
