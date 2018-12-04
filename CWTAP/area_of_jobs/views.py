from cwtap.core import viewsets
from .models import AreaOfJob
from .serializers import AreaOfJobSerializer


class AreaOfJobViewSet(viewsets.CWTAPViewSet):
    queryset = AreaOfJob.objects.all()
    serializer_class = AreaOfJobSerializer
    query_fields = ["name", "code", "status", "created",
                    "modified", "owner", "tenant"]
