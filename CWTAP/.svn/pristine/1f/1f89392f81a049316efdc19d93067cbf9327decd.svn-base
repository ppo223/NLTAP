from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "corpus"

router = routers.DefaultRouter()
router.register(r"corpusbase", views.CorpusBaseViewSet)
router.register(r"corpus", views.CorpusViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
