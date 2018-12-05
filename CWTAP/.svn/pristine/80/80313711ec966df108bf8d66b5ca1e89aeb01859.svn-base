from cwtap.core import viewsets
from .models import ModelBase, Model, ModelInstance
from .serializers import ModelBaseSerializer, \
    ModelSerializer, ModelInstanceSerializer


class ModelBaseViewSet(viewsets.CWTAPViewSet):
    queryset = ModelBase.objects.all()
    serializer_class = ModelBaseSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "area_of_job", "owner", "tenant"]


class ModelViewSet(viewsets.CWTAPViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    query_fields = ["name", "code", "details", "status", "created",
                    "modified", "modelbase", "owner", "tenant"]


class ModelInstanceViewSet(viewsets.CWTAPViewSet):
    queryset = ModelInstance.objects.all()
    serializer_class = ModelInstanceSerializer
    query_fields = ["name", "type", "details", "status",
                    "model", "created", "modified",
                    "storage_location", "storage_conflict_strategy",
                    "algorithm_instance", "owner", "tenant"]