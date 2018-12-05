from cwtap.core import viewsets
from .models import Dataset
from .serializers import DatasetSerializer


class DatasetViewSet(viewsets.CWTAPViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    query_fields = ["uuid", "generate_method", "generate_rules",
                    "storage_location", "business_data", "created",
                    "modified", "meta", "owner", "tenant"]
