from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Tenant(models.Model):
    """ 租户表 """
    name = models.CharField("租户名称", max_length=255)
    code = models.CharField("租户代码", max_length=255)
    status = models.IntegerField(
        "租户状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    type = models.CharField("租户类型", max_length=255)
    details = models.TextField("租户详情", default="")
    created = models.DateTimeField("租户创建时间", auto_now_add=True)
    modified = models.DateTimeField("租户修改时间", auto_now=True)
    owner = models.IntegerField("创建人", blank=True, default=0)
    tenant = models.IntegerField("租户", blank=True, default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """ 用户扩展表 """
    code = models.CharField("用户代码", max_length=255)
    status = models.IntegerField(
        "用户状态",
        choices=settings.STATUS_CHOICES,
        default=settings.STATUS_ENABLE)
    created = models.DateTimeField("用户创建时间", auto_now_add=True)
    modified = models.DateTimeField("用户修改时间", auto_now=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.IntegerField("创建人", blank=True, default=0)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
