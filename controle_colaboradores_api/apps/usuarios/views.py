from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth.models import Group

from .models import CustomUsuario, PasswordResetToken
from .serializers import GroupSerializer, CustomUsuarioSerializer, PasswordResetTokenSerializer
from .views_access_policies import GroupAccessPolicy, CustomUsuarioAccessPolicy, PasswordResetTokenAccessPolicy


class CustomUsuarioViewSet(ModelViewSet):
    permission_classes = (CustomUsuarioAccessPolicy,)
    serializer_class = CustomUsuarioSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return CustomUsuario.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    @action(detail=True, methods=['patch'])
    def criar_nova_password_apos_reset(self, request, pk=None):
        usuario = self.get_object()
        token = request.query_params['token']
        serializer = CustomUsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            usuario.set_password(serializer.validated_data['password'])
            usuario.save()
            serializer_token = PasswordResetTokenSerializer(data={'token': f'{token}'})
            if serializer_token.is_valid():
                usuario.password_reset_tokens.get(token=token).update(ativo=False)
            return Response({'status': 'A nova senha foi registrada.'})

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def mudar_password(self, request, pk=None):
        usuario = self.get_object()
        serializer = CustomUsuarioSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'A nova senha foi registrada.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(ModelViewSet):
    permission_classes = (GroupAccessPolicy,)
    serializer_class = GroupSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return Group.objects.all()


class PasswordResetTokenViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                GenericViewSet):
    permission_classes = (PasswordResetTokenAccessPolicy,)
    serializer_class = PasswordResetTokenSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return PasswordResetToken.objects.all()
