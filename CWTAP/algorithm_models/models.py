from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from users.models import Tenant
from area_of_jobs.models import AreaOfJob


class ModelBase(models.Model):
    """ 模型库表 """
    name = models.CharField("模型库名称", max_length=255)
    code = models.CharField("模型库代码", max_length=255)
    details = models.TextField("模型库详情", default="")
    status = models.IntegerField(
        "模型库状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("模型库创建时间", auto_now_add=True)
    modified = models.DateTimeField("模型库修改时间", auto_now=True)
    area_of_job = models.ForeignKey(
        AreaOfJob, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    """ 模型表 """
    name = models.CharField("模型名称", max_length=255)
    code = models.CharField("模型代码", max_length=255)
    type = models.CharField("模型类型", max_length=255, default="")
    details = models.TextField("模型详情", default="")
    status = models.IntegerField(
        "模型状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("模型创建时间", auto_now_add=True)
    modified = models.DateTimeField("模型修改时间", auto_now=True)
    modelbase = models.ForeignKey(ModelBase, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class ModelInstance(models.Model):
    """ 模型实例表 """
    uuid = models.CharField("模型实例号", max_length=255)
    name = models.CharField("模型实例名称", max_length=255)
    status = models.IntegerField(
        "模型实例状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    details = models.TextField("模型实例详情", default="")
    storage_location = models.CharField("实例存储位置", max_length=255, default="")
    storage_conflict_strategy = models.CharField(
        "实例存储冲突", max_length=20, default="")
    created = models.DateTimeField("实例创建时间", auto_now_add=True)
    modified = models.DateTimeField("实例修改时间", auto_now=True)
    algorithm_instance = models.IntegerField("算法实例id", default=0)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, blank=True, null=True)
