from rest_framework.routers import DefaultRouter

from .views import MunicipioViewSet

router = DefaultRouter()
router.register(r'municipios', MunicipioViewSet, basename='municipios')
