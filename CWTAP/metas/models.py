from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Tenant
from corpus.models import CorpusBase


class Meta(models.Model):
    """ 元数据表 """
    name = models.CharField("元数据名称", max_length=255)
    code = models.CharField("元数据代码", max_length=255)
    status = models.IntegerField(
        "元数据状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("元数据创建时间", auto_now_add=True)
    modified = models.DateTimeField("元数据修改时间", auto_now=True)
    corpusbase = models.ForeignKey(CorpusBase, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
