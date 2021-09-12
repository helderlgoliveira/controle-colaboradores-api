from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Perfil
from .serializers import PerfilSerializer
from .views_access_policies import PerfilAccessPolicy


class ArticleViewSet(ModelViewSet):
    permission_classes = (PerfilAccessPolicy, )
    serializer_class = PerfilSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        initial_queryset = Perfil.objects.all()
        return self.access_policy.scope_queryset(
            self.request, initial_queryset
        )
