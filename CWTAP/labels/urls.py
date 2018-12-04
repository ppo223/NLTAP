from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "labels"
router = routers.DefaultRouter()
router.register(r"labelbase", views.LabelBaseViewSet)
router.register(r"label", views.LabelViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
