from rest_framework.routers import DefaultRouter

from .views import (
    PerfilViewSet,
    EnderecoViewSet,
    TelefoneViewSet,
    OutroEmailViewSet,
    CargoViewSet,
    DepartamentoViewSet
)

router = DefaultRouter()
router.register(r'perfis', PerfilViewSet, basename='perfil')
router.register(r'enderecos', EnderecoViewSet, basename='endereco')
router.register(r'telefones', TelefoneViewSet, basename='telefone')
router.register(r'telefones', OutroEmailViewSet, basename='outroemail')
router.register(r'cargos', CargoViewSet, basename='cargo')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')