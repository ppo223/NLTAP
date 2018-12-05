from cwtap.core import viewsets
from .models import Meta
from .serializers import MetaSerializer


class MetaViewSet(viewsets.CWTAPViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer
    query_fields = ["name", "code", "status", "created",
                    "modified", "corpusbase", "owner", "tenant"]
