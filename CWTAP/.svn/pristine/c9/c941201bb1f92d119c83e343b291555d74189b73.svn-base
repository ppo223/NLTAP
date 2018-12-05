from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = "management"

router = routers.DefaultRouter()
router.register(r'tenant', views.TenantViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
