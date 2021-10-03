from rest_framework import mixins, status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_access_policy import AccessViewSetMixin

from .models import (
    Perfil,
    Endereco,
    Telefone,
    OutroEmail,
    Cargo,
    Departamento
)
from .serializers import (
    PerfilSerializer,
    EnderecoSerializer,
    TelefoneSerializer,
    OutroEmailSerializer,
    CargoSerializer,
    CargoMudarAtivacaoSerializer,
    DepartamentoSerializer,
    DepartamentoMudarAtivacaoSerializer
)
from .views_access_policies import (
    PerfilAccessPolicy,
    DadosParaContatoAccessPolicy,
    CargoAccessPolicy,
    DepartamentoAccessPolicy
)


class PerfilViewSet(AccessViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    Gerenciar os perfis dos usuários.
    """
    access_policy = PerfilAccessPolicy
    serializer_class = PerfilSerializer
    model = Perfil

    def get_queryset(self):
        return self.model.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)


class EnderecoViewSet(AccessViewSetMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = EnderecoSerializer
    model = Endereco

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )


class TelefoneViewSet(AccessViewSetMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = TelefoneSerializer
    model = Telefone

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OutroEmailViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = OutroEmailSerializer
    model = OutroEmail

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )


class CargoViewSet(AccessViewSetMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    access_policy = CargoAccessPolicy
    serializer_class = CargoSerializer
    model = Cargo

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    @action(detail=True, methods=['patch'], serializer_class=CargoMudarAtivacaoSerializer)
    def ativar(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(
            cargo,
            data={'ativo': True},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Cargo desativado.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=CargoMudarAtivacaoSerializer)
    def desativar(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(
            cargo,
            data={'ativo': False},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Cargo desativado.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class DepartamentoViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = DepartamentoAccessPolicy
    serializer_class = DepartamentoSerializer
    model = Departamento

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    @action(detail=True, methods=['patch'], serializer_class=DepartamentoMudarAtivacaoSerializer)
    def ativar(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(
            cargo,
            data={'ativo': True},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Cargo desativado.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=DepartamentoMudarAtivacaoSerializer)
    def desativar(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(
            cargo,
            data={'ativo': False},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Cargo desativado.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
