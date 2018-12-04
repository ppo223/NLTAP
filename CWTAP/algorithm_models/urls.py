from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "algorithm_models"

router = routers.DefaultRouter()
router.register(r"modelbase", views.ModelBaseViewSet)
router.register(r"model", views.ModelViewSet)
router.register(r"model_instance", views.ModelInstanceViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
