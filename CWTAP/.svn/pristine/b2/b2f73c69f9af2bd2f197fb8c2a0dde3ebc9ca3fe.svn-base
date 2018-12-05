from cwtap.core import viewsets
from .models import LabelBase, Label
from .serializers import LabelBaseSerializer, LabelSerializer


class LabelBaseViewSet(viewsets.CWTAPViewSet):
    queryset = LabelBase.objects.all()
    serializer_class = LabelBaseSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "area_of_job", "owner", "tenant"]


class LabelViewSet(viewsets.CWTAPViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    query_fields = ["name", "code", "status", "created", "modified",
                    "parent", "is_leaf", "labelbase", "owner", "tenant",
                    "originate_object", "originate_object_id"]
