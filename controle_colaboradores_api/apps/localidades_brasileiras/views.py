from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_access_policy import AccessViewSetMixin

from .models import Municipio
from .serializers import MunicipioSerializer
from .views_access_policies import MunicipioAccessPolicy


class MunicipioViewSet(AccessViewSetMixin, ReadOnlyModelViewSet):
    """
    Municipio ViewSet description:

    list: Listar municípios.
    retrieve: Consultar município.
    """
    access_policy = MunicipioAccessPolicy
    serializer_class = MunicipioSerializer

    def get_queryset(self):
        return Municipio.objects.all().order_by("id")
