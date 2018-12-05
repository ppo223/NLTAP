from cwtap.core import viewsets
from .models import CorpusBase, Corpus
from .serializers import CorpusBaseSerializer, CorpusSerializer


class CorpusBaseViewSet(viewsets.CWTAPViewSet):
    queryset = CorpusBase.objects.all()
    serializer_class = CorpusBaseSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "area_of_job", "owner", "tenant"]


class CorpusViewSet(viewsets.CWTAPViewSet):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer
    query_fields = ["corpus_type", "originate_object",
                    "originate_object_id",
                    "corpusbase", "owner", "tenant"]

