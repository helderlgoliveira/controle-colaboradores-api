from rest_framework.viewsets import ModelViewSet

from .models import Municipio
from .serializers import MunicipioSerializer
from .views_access_policies import MunicipioAccessPolicy


class MunicipioViewSet(ModelViewSet):
    permission_classes = (MunicipioAccessPolicy, )
    serializer_class = MunicipioSerializer

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        return Municipio.objects.all()
