from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = "rules"

router = routers.DefaultRouter()
router.register(r"rulebase", views.RuleBaseViewSet)
router.register(r"rule", views.RuleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
