from cwtap.core import viewsets
from .models import RuleBase, Rule
from .serializers import RuleBaseSerializer, RuleSerializer


class RuleBaseViewSet(viewsets.CWTAPViewSet):
    queryset = RuleBase.objects.all()
    serializer_class = RuleBaseSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "area_of_job", "owner", "tenant"]


class RuleViewSet(viewsets.CWTAPViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    query_fields = ["expression", "status", "created", "modified",
                    "label", "originate_object", "originate_object_id",
                    "rulebase", "owner", "tenant"]