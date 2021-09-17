from rest_framework.viewsets import ModelViewSet

from .models import Perfil
from .serializers import PerfilSerializer
from .views_access_policies import PerfilAccessPolicy


class PerfilViewSet(ModelViewSet):
    permission_classes = (PerfilAccessPolicy, )
    serializer_class = PerfilSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return Perfil.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario_modificacao=self.request.user)
