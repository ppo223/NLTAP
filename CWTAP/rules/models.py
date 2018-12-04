from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Tenant
from area_of_jobs.models import AreaOfJob
from labels.models import Label


class RuleBase(models.Model):
    """ 规则库表 """
    name = models.CharField("规则库名称", max_length=255)
    code = models.CharField("规则库代码", max_length=255)
    details = models.TextField("规则库详情", default="")
    status = models.IntegerField(
        "规则库状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("规则库创建时间", auto_now_add=True)
    modified = models.DateTimeField("规则库修改时间", auto_now=True)
    area_of_job = models.ForeignKey(
        AreaOfJob, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Rule(models.Model):
    """ 规则表 """
    expression = models.TextField("规则表达", default="")
    status = models.IntegerField(
        "规则状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("规则创建时间", auto_now_add=True)
    modified = models.DateTimeField("规则修改时间", auto_now=True)
    label = models.ForeignKey(
        Label, on_delete=models.CASCADE)
    originate_object = models.CharField("规则来源", max_length=255, default="")
    originate_object_id = models.IntegerField(
        "规则来源编号", default=0)
    rulebase = models.ForeignKey(RuleBase, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.expression
