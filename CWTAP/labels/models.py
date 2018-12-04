from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Tenant
from area_of_jobs.models import AreaOfJob


class LabelBase(models.Model):
    """ 标签库表 """
    name = models.CharField("标签库名称", max_length=255)
    code = models.CharField("标签库代码", max_length=255)
    type = models.CharField("标签库类型", max_length=255, default="")
    details = models.TextField("标签库详情", default="")
    status = models.IntegerField(
        "标签库状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("标签库创建时间", auto_now_add=True)
    modified = models.DateTimeField("标签库修改时间", auto_now=True)
    area_of_job = models.ForeignKey(
        AreaOfJob, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    """ 标签表 """
    name = models.CharField("标签名称", max_length=255)
    code = models.CharField("标签代码", max_length=255)
    status = models.IntegerField(
        "标签状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("标签创建时间", auto_now_add=True)
    modified = models.DateTimeField("标签修改时间", auto_now=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True)
    is_leaf = models.BooleanField("标签是否为叶子节点", default=True)
    labelbase = models.ForeignKey(LabelBase, on_delete=models.CASCADE)
    originate_object = models.CharField("标签来源", max_length=255, default="")
    originate_object_id = models.IntegerField("标签来源编号", default=0)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)
