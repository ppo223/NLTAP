from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "metas"
router = routers.DefaultRouter()
router.register(r"meta", views.MetaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
