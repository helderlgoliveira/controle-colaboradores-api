from rest_framework.routers import SimpleRouter

from .views import PerfilViewSet

router = SimpleRouter()
router.register(r'perfis', PerfilViewSet, basename='perfis')
urlpatterns = router.urls
