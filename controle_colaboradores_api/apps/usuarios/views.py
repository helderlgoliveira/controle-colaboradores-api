from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth.models import Group

from .models import CustomUsuario, PasswordResetToken
from .serializers import GroupSerializer, CustomUsuarioSerializer, PasswordResetTokenSerializer, PasswordSerializer
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
        user = self.get_object()
        token = request.query_params['token']
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            serializer_token = PasswordResetTokenSerializer(data={'token': f'{token}'})
            if serializer_token.is_valid():
                user.password_reset_tokens.get(token=token).update(ativo=False)
            return Response({'status': 'nova senha cadastrada.'})

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def mudar_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('senha_atual')):
                return Response({'senha_atual': ['Senha incorreta.']},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('nova_senha'))
            user.save()
            return Response({'status': 'nova senha cadastrada.'}, status=status.HTTP_200_OK)

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
