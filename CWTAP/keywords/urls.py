from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "keywords"

router = routers.DefaultRouter()
router.register(r"keywordbase", views.KeywordBaseViewSet)
router.register(r"keyword", views.KeywordViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
