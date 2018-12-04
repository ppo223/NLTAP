from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "knowledge_graphs"

router = routers.DefaultRouter()
router.register(r"knowledgebase", views.KnowledgeGraphBaseViewSet)
router.register(r"knowledge", views.KnowledgeGraphViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
