from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "tasks"

router = routers.DefaultRouter()
router.register(r"task", views.ModelTaskViewSet)
router.register(r"task_execution", views.ModelTaskExecutionViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
