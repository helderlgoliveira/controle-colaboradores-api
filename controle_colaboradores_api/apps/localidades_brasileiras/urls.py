from rest_framework.routers import SimpleRouter

from .views import MunicipioViewSet

router = SimpleRouter()
router.register(r'municipios', MunicipioViewSet, basename='municipios')
urlpatterns = router.urls

print(urlpatterns)
