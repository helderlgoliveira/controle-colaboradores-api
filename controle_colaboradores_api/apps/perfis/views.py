from rest_framework.viewsets import ModelViewSet
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
    DepartamentoSerializer
)
from .views_access_policies import (
    PerfilAccessPolicy,
    DadosParaContatoAccessPolicy,
    CargoAccessPolicy,
    DepartamentoAccessPolicy
)


class PerfilViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = PerfilAccessPolicy
    serializer_class = PerfilSerializer
    model = Perfil

    def get_queryset(self):
        return self.model.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)


class EnderecoViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = EnderecoSerializer
    model = Endereco

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )


class TelefoneViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = TelefoneSerializer
    model = Telefone

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )


class OutroEmailViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = DadosParaContatoAccessPolicy
    serializer_class = OutroEmailSerializer
    model = OutroEmail

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )


class CargoViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = CargoAccessPolicy
    serializer_class = CargoSerializer
    model = Cargo

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )


class DepartamentoViewSet(AccessViewSetMixin, ModelViewSet):
    access_policy = DepartamentoAccessPolicy
    serializer_class = DepartamentoSerializer
    model = Departamento

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, self.model.objects.all()
        )
