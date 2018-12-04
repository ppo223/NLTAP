from cwtap.core import viewsets
from .models import ModelTask, ModelTaskExecution
from .serializers import ModelTaskSerializer, ModelTaskExecutionSerializer


class ModelTaskViewSet(viewsets.CWTAPViewSet):
    queryset = ModelTask.objects.all()
    serializer_class = ModelTaskSerializer
    query_fields = ["name", "type", "schedule_rule", "details",
                    "status", "created", "modified",
                    "dataset_generate_method", "dataset_generate_rule",
                    "model_instance", "owner", "tenant"]


class ModelTaskExecutionViewSet(viewsets.CWTAPViewSet):
    queryset = ModelTaskExecution.objects.all()
    serializer_class = ModelTaskExecutionSerializer
    query_fields = ["status", "result", "started",
                    "ended", "created", "modified",
                    "train_task", "dataset", "tenant"]

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.userprofile.tenant)

    def perform_update(self, serializer):
        serializer.save(
            tenant=self.request.user.userprofile.tenant)
