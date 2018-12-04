from cwtap.core import viewsets
from .models import KnowledgeGraphBase, KnowledgeGraph
from .serializers import KnowledgeGraphBaseSerializer, KnowledgeGraphSerializer


class KnowledgeGraphBaseViewSet(viewsets.CWTAPViewSet):
    queryset = KnowledgeGraphBase.objects.all()
    serializer_class = KnowledgeGraphBaseSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "area_of_job", "owner", "tenant"]


class KnowledgeGraphViewSet(viewsets.CWTAPViewSet):
    queryset = KnowledgeGraph.objects.all()
    serializer_class = KnowledgeGraphSerializer
    query_fields = ["originate_object", "originate_object_id",
                    "knowledgebase", "owner", "tenant"]