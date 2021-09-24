from rest_framework.routers import DefaultRouter

from .views import CustomUsuarioViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'usuarios', CustomUsuarioViewSet, basename='usuarios')
router.register(r'grupos', GroupViewSet, basename='grupos')
