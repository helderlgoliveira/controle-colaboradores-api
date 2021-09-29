from rest_framework.routers import DefaultRouter

from .views import CustomUsuarioViewSet, GroupViewSet, PasswordResetTokenViewSet

router = DefaultRouter()
router.register(r'usuarios', CustomUsuarioViewSet, basename='customusuario')
router.register(r'grupos', GroupViewSet, basename='group')
router.register(r'pwd-reset-tokens', PasswordResetTokenViewSet, basename='passwordresettoken')
