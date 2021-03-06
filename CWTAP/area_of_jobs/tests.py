import json

from rest_framework import status
from django.urls import reverse

from cwtap.core.test import CWTAPAPITestCase
from area_of_jobs.models import AreaOfJob


class AreaOfJobTest(CWTAPAPITestCase):
    """ 测试机构领域表 """

    def test_aoj_create(self):
        """ 测试创建机构领域 """
        url = reverse("area_of_job:areaofjob-list")
        data = {"name": "机构01", "code": "jigou01"}
        response = self.client.post(url, data, **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response.content)
        self.assertEqual(data["name"], response_data["name"])
        self.assertEqual(self.users[0].id, response_data["owner"])
        self.assertEqual(self.tenants[0].id, response_data["tenant"])

        response = self.client.get(url, data, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual("jigou01", json.loads(response.content)[0]['code'])

    def test_aoj_delete(self):
        """ 测试机构领域删除 """
        aojs = self.create_instances([
            {"name": "机构02", "code": "jigou02"},
            {"name": "机构03", "code": "jigou03"}
        ], "AreaOfJob")

        self.assertEqual(2, len(AreaOfJob.objects.all()))
        self.assertEqual(aojs[0].name,
                         AreaOfJob.objects.get(id=aojs[0].id).name)

        url = reverse("area_of_job:areaofjob-detail", args=(aojs[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT,
                         response.content)
        self.assertEqual(1, len(AreaOfJob.objects.all()))
        self.assertEqual(aojs[1].name,
                         AreaOfJob.objects.get(id=aojs[1].id).name)

    def test_aoj_update(self):
        """ 测试修改机构领域 """
        aojs = self.create_instances([
            {"name": "机构_0401", "code": "jigou_0401"},
            {"name": "机构_0402", "code": "jigou_0402"}
        ], "AreaOfJob")

        self.assertEqual(2, len(AreaOfJob.objects.all()))
        self.assertEqual(aojs[0].name,
                         AreaOfJob.objects.get(id=aojs[0].id).name)
        self.assertTrue(aojs[0].owner is None)
        self.assertTrue(aojs[0].tenant is None)
        self.assertEqual(aojs[0].owner, aojs[1].owner)
        self.assertEqual(aojs[0].tenant, aojs[1].tenant)

        url = reverse("area_of_job:areaofjob-detail", args=(aojs[1].id,))
        data = {
            "name": "机构_0402修改",
            "code": "jigou_0402修改"
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(data["name"],
                         AreaOfJob.objects.get(id=aojs[1].id).name)
        self.assertEqual(aojs[0].name,
                         AreaOfJob.objects.get(id=aojs[0].id).name)
        self.assertEqual(self.users[0],
                         AreaOfJob.objects.get(id=aojs[1].id).owner)
        self.assertEqual(self.tenants[0],
                         AreaOfJob.objects.get(id=aojs[1].id).tenant)
        self.assertTrue(AreaOfJob.objects.get(id=aojs[0].id).owner is None)
        self.assertTrue(AreaOfJob.objects.get(id=aojs[0].id).tenant is None)

    def test_aoj_query(self):
        """ 测试查询机构领域 """
        url = reverse("area_of_job:areaofjob-list")
        data = {
            "name": "机构05",
            "code": "jigou05"
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response.content)

        response = self.client.get(url, **self.auth_header)

        self.assertEqual(data["name"], json.loads(response.content)[0]["name"])

    def test_aoj_user_relations(self):
        """ 测试机构领域与用户与租户关联关系 """
        tenant = self.tenants[0]
        user = self.users[0]
        aojs = self.create_instances([
            {
                "name": "机构07",
                "code": "jigou07",
                "owner": user,
                "tenant": tenant
            },
            {
                "name": "机构08",
                "code": "jigou08",
                "owner": user,
                "tenant": tenant
            }
        ], "AreaOfJob")

        # 测试机构领域和租户间的关系
        self.assertEqual(aojs[0].tenant, aojs[1].tenant)
        self.assertEqual(aojs[0].tenant.name, tenant.name)
        # 测试机构领域和用户间的关系
        self.assertEqual(aojs[0].owner, aojs[1].owner)
        self.assertEqual(aojs[0].owner.username, user.username)
        # 测试机构领域中租户和用户间的关系
        self.assertEqual(tenant.name, user.userprofile.tenant.name)
        self.assertEqual(aojs[1].owner.userprofile.tenant.name, tenant.name)
