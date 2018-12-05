import json
import time

from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework import status

from cwtap.core.test import CWTAPAPITestCase
from users.models import Tenant, UserProfile


class TenantTest(CWTAPAPITestCase):
    """ 测试租户表 """

    def test_create_tenant(self):
        """ 测试租户创建 """
        data = {
            "name": "租户_001",
            "code": "tenant_001",
            "type": "类型_001",
            "details": "这里是租户_001"
        }
        response = self.client.post(reverse("management:tenant-list"),
                                    data,
                                    **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response.content)

        pk = json.loads(response.content)["id"]
        t = Tenant.objects.get(pk=pk)

        self.assertEqual(data["name"], t.name)
        self.assertEqual(data["code"], t.code)
        self.assertEqual(data["type"], t.type)
        self.assertEqual(data["details"], t.details)
        self.assertEqual(settings.STATUS_ENABLE, t.status)

    def test_list_tenant(self):
        """ 测试获取租户列表 """
        response = self.client.get(reverse("management:tenant-list"),
                                   **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(2, len(json.loads(response.content)))

    def test_update_tenant(self):
        """ 测试更新租户 """
        tenant_004 = model_to_dict(self.tenants[0])

        self.assertEqual(self.tenants[0].name, tenant_004["name"])

        url = reverse("management:tenant-detail", args=(tenant_004["id"],))
        tenant_004["name"] = "租户_004_修改"
        response = self.client.put(url, tenant_004, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("租户_004_修改",
                         Tenant.objects.get(pk=tenant_004["id"]).name)

    def test_tenant_update_auto_now(self):
        """ 测试 modified 字段 auto_now 属性 """
        tenant = self.tenants[0]
        created, modified = tenant.created, tenant.modified
        time.sleep(1)
        tenant.name = "租户_006_修改"
        tenant.save()

        self.assertEqual(tenant.created, created)
        self.assertTrue(tenant.modified > modified)

    def test_delete_tenant(self):
        """ 测试删除租户 """
        tenant = self.tenants[0]
        url = reverse("management:tenant-detail", args=(tenant.id,))

        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(url, **self.auth_header).status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_query_tenant(self):
        """ 测试查询租户 """
        url = "{0}?{1}".format(reverse("management:tenant-list"),
                               "name={0}".format(self.tenants[0].name))

        response = self.client.get(url, **self.auth_header)

        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(query_result))
        self.assertEqual(self.tenants[0].name, query_result[0]["name"])

    def test_query_type_tenant(self):
        """ 测试查询租户类型 """
        tenants = self.create_instances([
            {
                "name": "租户_010",
                "code": "tenant_010",
                "type": "类型_010"
            },
            {
                "name": "租户_011",
                "code": "tenant_011",
                "type": "类型_010"
            }
        ], "Tenant")

        url = "{0}?{1}".format(reverse("management:tenant-list"),
                               "type={0}".format(tenants[0].type))
        response = self.client.get(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(json.loads(response.content)))

    def test_query_status_tenant(self):
        """ 测试查询租户状态 """
        url = "{0}?{1}".format(reverse("management:tenant-list"),
                               "status={0}".format(settings.STATUS_ENABLE))
        response = self.client.get(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 默认是启用状态
        self.assertEqual(2, len(json.loads(response.content)))

    def test_query_created_tenant(self):
        """ 测试查询租户创建时间 """
        url = "{0}?{1}".format(reverse("management:tenant-list"),
                               "created= to {0}".format(timezone.now()))
        response = self.client.get(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(json.loads(response.content)))

    def test_query_modified_tenant(self):
        """ 测试查询用户修改时间 """
        time.sleep(1)
        now = timezone.now()
        time.sleep(1)
        self.tenants[0].name = "租户_016_修改"
        self.tenants[0].save()

        # 查 租户_016
        url = "{0}?{1}".format(reverse("management:tenant-list"),
                               "modified={0} to".format(now))
        response = self.client.get(url, **self.auth_header)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(result))
        self.assertEqual(self.tenants[0].name, result[0]["name"])

        # 查 租户_017
        url = "{0}?{1}".format(reverse("management:tenant-list"),
                               "modified=to {0}".format(now))
        response = self.client.get(url, **self.auth_header)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(result))
        self.assertEqual(self.tenants[1].name, result[0]["name"])


class UserTest(CWTAPAPITestCase):

    def test_create_user(self):
        """ 测试创建用户 """
        url = reverse("management:user-list")
        data = {
            "username": "用户_001",
            "email": "user_001@mail.com",
            "password": "user123",
            "userprofile": {
                "code": "user_001",
                "tenant": self.tenants[0].id
            }
        }
        response = self.client.post(url,
                                    json.dumps(data),
                                    content_type="application/json",
                                    **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response_data)
        self.assertEqual(data["username"], response_data["username"])
        self.assertEqual(data["email"], response_data["email"])
        self.assertEqual(data["userprofile"]["tenant"],
                         response_data["userprofile"]["tenant"])
        self.assertEqual(response_data["id"],
                         response_data["userprofile"]["user"])

        user_tenant = User.objects.get(
            pk=response_data["id"]).userprofile.tenant

        self.assertEqual(self.tenants[0].name, user_tenant.name)
        self.assertEqual(self.tenants[0].code, user_tenant.code)
        self.assertEqual(self.tenants[0].type, user_tenant.type)

    def test_user_relations(self):
        """ 测试用户关系 """
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)

    def test_user_none_tenant(self):
        """ 测试创建用户不含租户编号 """
        url = reverse("management:user-list")
        data = {
            "username": "用户_001",
            "email": "user_001@mail.com",
            "password": "user123",
            "userprofile": {
                "code": "user_001"
            }
        }
        response = self.client.post(url,
                                    json.dumps(data),
                                    content_type="application/json",
                                    **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         response.content)
        self.assertTrue(
            b"tenant" in response.content)
        self.assertTrue(
            b"This field is required" in response.content)

    def test_list_user(self):
        """ 测试用户列表 """
        response = self.client.get(reverse("management:user-list"),
                                   **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(2, len(response_data))
        self.assertEqual(response_data[0]["userprofile"]["code"],
                         self.user_profiles[0].code)
        self.assertEqual(response_data[1]["userprofile"]["code"],
                         self.user_profiles[1].code)

    def test_update_user(self):
        """ 测试更新用户 """
        user = self.users[0]

        self.assertEqual(self.tenants[0].id,
                         user.userprofile.tenant.id)

        modified = user.userprofile.modified
        data = {
            "username": user.username,
            "email": user.email,
            "userprofile": {
                "code": user.userprofile.code,
                "owner": user.id,
                "tenant": self.tenants[1].id
            }
        }
        url = reverse("management:user-detail", args=(user.id,))
        response = self.client.put(url,
                                   json.dumps(data),
                                   content_type="application/json",
                                   **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(self.tenants[1].id,
                         response_data["userprofile"]["tenant"])
        self.assertTrue(User.objects.get(
            pk=response_data["id"]).userprofile.modified > modified)

    def test_delete_user(self):
        """ 测试删除用户 """
        url = reverse("management:user-detail", args=(self.users[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT,
                         response.content)

        users = User.objects.all()
        userprofiles = UserProfile.objects.all()

        self.assertEqual(1, len(users))
        self.assertEqual(1, len(userprofiles))
        self.assertEqual(users[0].userprofile, userprofiles[0])
