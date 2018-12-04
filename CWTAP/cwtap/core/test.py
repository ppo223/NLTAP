import random
import json

from django.conf import settings
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from cwtap.core.utils import Utils


class CWTAPAPITestCaseBase(APITestCase):

    def create_instances(self, instances, class_name):
        class_name = class_name.lower()
        result, relations = [], Utils.get_model_app_relations()
        for instance in instances:
            if class_name == "user":
                i = User.objects.create_user(**instance)
            else:
                ModelClass = apps.get_model(relations[class_name], class_name)
                i = ModelClass.objects.create(**instance)

            i.save()
            result.append(i)

        return result

    def random_value(self, value):
        return "{0}_{1}".format(value, random.random())

    def setUp(self):
        self.tenants = self.create_instances([
            {
                "name": self.random_value("租户_001"),
                "code": self.random_value("tenant_001"),
                "type": self.random_value("类型_001")
            },
            {
                "name": self.random_value("租户_002"),
                "code": self.random_value("tenant_002"),
                "type": self.random_value("类型_002")
            }
        ], "Tenant")

        self.users_data = [
            {
                "username": self.random_value("user_001"),
                "email": self.random_value("user_001") + "@mail.com",
                "password": self.random_value("user_001"),
            },
            {
                "username": self.random_value("user_002"),
                "email": self.random_value("user_002") + "@mail.com",
                "password": self.random_value("user_002"),
            },
        ]
        self.users = self.create_instances(self.users_data, "User")

        self.user_profiles = self.create_instances([
            {
                "code": self.random_value("user_001"),
                "user": self.users[0],
                "tenant": self.tenants[0]
            },
            {
                "code": self.random_value("user_002"),
                "user": self.users[1],
                "tenant": self.tenants[1]
            },
        ], "UserProfile")


class CWTAPAPITestCase(CWTAPAPITestCaseBase):

    def setUp(self):
        # 初始化用户、租户数据
        super().setUp()
        # 创建应用
        Utils.init_password_grant_application()
        # 根据账号和密码获取Token
        response = self.client.post(
            reverse("oauth2_provider:token"),
            data={
                "grant_type": "password",
                "username": self.users[0].username,
                "password": self.users_data[0]["password"],
            },
            **Utils.get_basic_auth_header(
                settings.CLIENT_ID,
                settings.CLIENT_SECRET
            )
        )
        response_data = json.loads(response.content)
        # 根据Token获取头信息
        self.auth_header = Utils.get_auth_header(response_data["access_token"])
