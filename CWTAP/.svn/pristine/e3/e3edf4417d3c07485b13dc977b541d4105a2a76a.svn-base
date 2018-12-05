from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Tenant


class AreaOfJob(models.Model):
    """ 机构领域表 """
    name = models.CharField("机构领域名称", max_length=255)
    code = models.CharField("机构领域代码", max_length=255)
    status = models.IntegerField(
        "机构领域状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("机构领域创建时间", auto_now_add=True)
    modified = models.DateTimeField("机构领域修改时间", auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
