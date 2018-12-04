from cwtap.core import viewsets
from .models import KeywordBase, Keyword
from .serializers import KeywordBaseSerializer, KeywordSerializer


class KeywordBaseViewSet(viewsets.CWTAPViewSet):
    queryset = KeywordBase.objects.all()
    serializer_class = KeywordBaseSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "area_of_job", "owner", "tenant"]


class KeywordViewSet(viewsets.CWTAPViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    query_fields = ["name", "pos", "emotion", "level", "synonym",
                    "statut", "originate_object_id", "keywordbase",
                    "originate_object", "tenant", "owner", "antonym"]