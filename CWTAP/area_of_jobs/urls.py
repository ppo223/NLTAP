from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "area_of_job"
router = routers.DefaultRouter()
router.register(r"aoj", views.AreaOfJobViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
