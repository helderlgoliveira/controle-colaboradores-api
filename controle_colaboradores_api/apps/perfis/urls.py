from rest_framework.routers import DefaultRouter

from .views import (
    PerfilViewSet,
    EnderecoViewSet,
    TelefoneViewSet,
    CargoViewSet,
    DepartamentoViewSet
)

router = DefaultRouter()
router.register(r'perfis', PerfilViewSet, basename='perfis')
router.register(r'enderecos', EnderecoViewSet, basename='enderecos')
router.register(r'telefones', TelefoneViewSet, basename='telefones')
router.register(r'cargos', CargoViewSet, basename='cargos')
router.register(r'departamentos', DepartamentoViewSet, basename='departamentos')