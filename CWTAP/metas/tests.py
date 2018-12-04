import json

from django.urls import reverse
from rest_framework import status

from cwtap.core.test import CWTAPAPITestCase


from .models import Meta


class MetaTest(CWTAPAPITestCase):
    """ 测试元数据表 """

    def setUp(self):
        super().setUp()
        self.corpusbase = self.create_instances([{
            "name": "语料库",
            "code": "corpusbase"
        }], "Corpusbase")[0]

    def test_meta_create(self):
        """ 测试元数据创建 """
        url = reverse("metas:meta-list")
        data = {
            "name": "元数据01",
            "code": "meta01",
            "corpusbase": self.corpusbase.id
        }

        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

    def test_meta_delete(self):
        """ 测试元数据删除 """
        metas = self.create_instances([
            {
                "name": "元数据02",
                "code": "meta02",
                "corpusbase": self.corpusbase
            },
            {
                "name": "元数据03",
                "code": "meta03",
                "corpusbase": self.corpusbase
            }
        ], "Meta")

        url = reverse("metas:meta-detail",
                      args=(metas[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(Meta.objects.all()))
        self.assertEqual(metas[1].name,
                         Meta.objects.get(id=metas[1].id).name)

    def test_meta_update(self):
        """ 测试元数据修改 """
        metas = self.create_instances([
            {
                "name": "元数据_0401",
                "code": "meta_0401",
                "corpusbase": self.corpusbase
            },
            {
                "name": "元数据_0402",
                "code": "meta_0402",
                "corpusbase": self.corpusbase
            }
        ], "Meta")

        url = reverse("metas:meta-detail",
                      args=(metas[1].id,))

        data = {
            "name": "元数据_0402_修改",
            "code": "meta_0402_修改",
            "corpusbase": self.corpusbase.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(metas[0].name,
                         Meta.objects.get(id=metas[0].id).name)

        url = reverse("metas:meta-list")
        response = self.client.get(url, **self.auth_header)

        self.assertEqual(data["name"],
                         json.loads(response.content)[1]["name"])
        self.assertEqual(metas[0].name,
                         json.loads(response.content)[0]["name"])

    def test__meta_query(self):
        """ 测试元数据查询 """
        metas = self.create_instances([
            {
                "name": "元数据_0501",
                "code": "meta_0501",
                "corpusbase": self.corpusbase
            },
            {
                "name": "元数据_0502",
                "code": "meta_0502",
                "corpusbase": self.corpusbase
            }
        ], "Meta")

        url = "{0}?{1}".format(reverse("metas:meta-list"),
                               "name=元数据_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(metas[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("metas:meta-list"),
                               "name=元数据_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(metas[1].name, query_result[0]["name"])

    def test_meta_corpus_user_relations(self):
        """ 测试元数据与语料库与用户与租户关联关系 """
        metas = self.create_instances([
            {
                "name": "元数据06",
                "code": "meta06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "corpusbase": self.corpusbase
            },
            {
                "name": "元数据07",
                "code": "meta07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "corpusbase": self.corpusbase
            }
        ], "Meta")

        # 测试元数据和租户间的关系
        self.assertTrue(not None, self.tenants[0].name)
        self.assertEqual(metas[0].tenant, metas[1].tenant)
        self.assertEqual(metas[0].tenant.name, self.tenants[0].name)
        # 测试元数据和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(metas[0].owner, metas[1].owner)
        self.assertEqual(metas[0].owner.username, self.users[0].username)
        # 测试元数据和语料库间的关系
        self.assertTrue(not None, self.corpusbase.name)
        self.assertEqual(metas[0].corpusbase, metas[1].corpusbase)
        self.assertEqual(metas[0].corpusbase.name, self.corpusbase.name)
        # 测试元数据中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(metas[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)
