from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
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
    Perfil ViewSet description:

    create: Criar perfil.
    retrieve: Consultar perfil.
    update: Atualizar perfil.
    partial_update: Atualizar parcialmente um perfil.
    list: Listar perfis.
    """
    access_policy = PerfilAccessPolicy
    serializer_class = PerfilSerializer
    model = Perfil

    def get_queryset(self):
        return self.model.objects.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    # Não há actions para Ativar e Desativar porque a manipulação
    # da ativação do perfil é feita pelas Views do app 'usuarios'


class EnderecoViewSet(AccessViewSetMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    Endereço ViewSet description:

    create: Criar endereço.
    retrieve: Consultar endereço.
    destroy: Deletar endereço.
    list: Listar endereços.
    """
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = EnderecoSerializer
    model = Endereco

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all().order_by('id')
        )


class TelefoneViewSet(AccessViewSetMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    Telefone ViewSet description:

    create: Criar telefone.
    retrieve: Consultar telefone.
    destroy: Deletar telefone.
    list: Listar telefones.
    """
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = TelefoneSerializer
    model = Telefone

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all().order_by('id')
        )


class OutroEmailViewSet(AccessViewSetMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """
    OutroEmail ViewSet description:

    create: Criar outro e-mail.
    retrieve: Consultar outro e-mail.
    destroy: Deletar outro e-mail.
    list: Listar outros e-mails.
    """
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = OutroEmailSerializer
    model = OutroEmail

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all().order_by('id')
        )


class CargoViewSet(AccessViewSetMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    Cargo ViewSet description:

    create: Criar cargo.
    retrieve: Consultar cargo.
    update: Atualizar cargo.
    partial_update: Atualizar parcialmente um cargo.
    list: Listar cargos.
    ativar: Ativar cargo.
    desativar: Desativar cargo.
    """
    access_policy = CargoAccessPolicy
    serializer_class = CargoSerializer
    model = Cargo

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all().order_by('id')
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
            return Response({'status': 'Cargo ativado.'},
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


class DepartamentoViewSet(AccessViewSetMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """
    Departamento ViewSet description:

    create: Criar departamento.
    retrieve: Consultar departamento.
    update: Atualizar departamento.
    partial_update: Atualizar parcialmente um departamento.
    list: Listar departamentos.
    ativar: Ativar departamento.
    desativar: Desativar departamento.
    """
    access_policy = DepartamentoAccessPolicy
    serializer_class = DepartamentoSerializer
    model = Departamento

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all().order_by('id')
        )

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    @action(detail=True, methods=['patch'], serializer_class=DepartamentoMudarAtivacaoSerializer)
    def ativar(self, request, pk=None):
        departamento = self.get_object()
        serializer = self.get_serializer(
            departamento,
            data={'ativo': True},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Departamento desativado.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=DepartamentoMudarAtivacaoSerializer)
    def desativar(self, request, pk=None):
        departamento = self.get_object()
        serializer = self.get_serializer(
            departamento,
            data={'ativo': False},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Departamento desativado.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
