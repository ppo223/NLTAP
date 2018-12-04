from cwtap.core import viewsets
from .models import Tenant, User
from .serializers import TenantSerializer, UserSerializer


class TenantViewSet(viewsets.CWTAPViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    query_fields = ["name", "code", "type", "status", "created", "modified"]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user.id,
            tenant=self.request.user.userprofile.tenant.id)

    def perform_update(self, serializer):
        serializer.save(
            owner=self.request.user.id,
            tenant=self.request.user.userprofile.tenant.id)


class UserViewSet(viewsets.CWTAPViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    query_fields = [
        "name", "code", "status", "type",
        "email", "owner", "created", "modified", "tenant"]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
