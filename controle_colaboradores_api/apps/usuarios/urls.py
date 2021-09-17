from rest_framework.routers import SimpleRouter

from .views import CustomUsuarioViewSet, GroupViewSet

router = SimpleRouter()
router.register(r'usuarios', CustomUsuarioViewSet, basename='usuarios')
router.register(r'grupos', GroupViewSet, basename='grupos')
urlpatterns = router.urls

print(urlpatterns)
