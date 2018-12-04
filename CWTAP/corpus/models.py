from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Tenant
from area_of_jobs.models import AreaOfJob


class CorpusBase(models.Model):
    """ 语料库表 """
    name = models.CharField("语料库名称", max_length=255)
    code = models.CharField("语料库代码", max_length=255)
    details = models.TextField("语料库详情", default="")
    status = models.IntegerField(
        "语料库状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("语料库创建时间", auto_now_add=True)
    modified = models.DateTimeField("语料库修改时间", auto_now=True)
    area_of_job = models.ForeignKey(
        AreaOfJob, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Corpus(models.Model):
    """ 语料表 """
    corpus_type = models.CharField("语料类型", max_length=255)
    originate_object = models.CharField("语料来源", max_length=255, default="")
    originate_object_id = models.IntegerField("语料来源编号", default=0)
    corpusbase = models.ForeignKey(CorpusBase, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.corpus_type
