import json

from django.urls import reverse
from rest_framework import status

from cwtap.core.test import CWTAPAPITestCase
from corpus.models import CorpusBase


class CorpusBaseTest(CWTAPAPITestCase):
    """ 测试语料库表 """

    def test_corpusbase_create(self):
        """ 测试语料库创建 """
        url = reverse("corpus:corpusbase-list")
        data = {
            "code": "corpusbase01",
            "details": "你好，语料库01"
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(["This field is required."],
                         json.loads(response.content)["name"])

        data["name"] = "语料库01"
        response = self.client.post(url, data, **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         response.content)
        self.assertEqual(data["name"], response_data["name"])
        self.assertEqual(self.users[0].id, response_data["owner"])
        self.assertEqual(self.tenants[0].id, response_data["tenant"])

        response = self.client.get(url, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(data["name"], json.loads(response.content)[0]["name"])

    def test_corpusbase_delete(self):
        """ 测试语料库删除 """
        corpusbases = self.create_instances([
            {
                "name": "语料库02",
                "code": "corpusbase02",
                "details": "你好，语料库02"
            },
            {
                "name": "语料库03",
                "code": "corpusbase03",
                "details": "你好，语料库03"
            }
        ], "CorpusBase")
        url = reverse("corpus:corpusbase-detail",
                      args=(corpusbases[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(1, len(CorpusBase.objects.all()))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("corpus:corpusbase-list")
        response_01 = self.client.get(url,
                                      {"name": corpusbases[0].name},
                                      **self.auth_header)
        response_02 = self.client.get(url,
                                      {"name": corpusbases[1].name},
                                      **self.auth_header)

        self.assertEqual(json.loads(response_01.content), [])
        self.assertEqual(json.loads(response_02.content)[0]["name"],
                         corpusbases[1].name)

    def test_corpusbase_update(self):
        """ 测试语料库修改 """
        corpusbases = self.create_instances([
            {
                "name": "语料库_0401",
                "code": "corpusbase_0401"
            },
            {
                "name": "语料库_0402",
                "code": "corpusbase_0402"
            }
        ], "CorpusBase")

        self.assertTrue(corpusbases[0].owner is None)
        self.assertTrue(corpusbases[0].tenant is None)

        url = reverse("corpus:corpusbase-detail", args=(corpusbases[1].id,))
        data = {
            "name": "语料库_0402_修改",
            "code": "corpusbase_0402_修改",
            "details": "你好，语料库_0402_修改"
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)

        url = reverse("corpus:corpusbase-list")
        response = self.client.get(url, **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(corpusbases[0].name, response_data[0]["name"])
        self.assertTrue(response_data[0]["owner"] is None)
        self.assertTrue(response_data[0]["tenant"] is None)
        self.assertEqual(data["name"], response_data[1]["name"])
        self.assertEqual(self.users[0].id, response_data[1]["owner"])
        self.assertEqual(self.tenants[0].id, response_data[1]["tenant"])

    def test_corpusbase_query(self):
        """ 测试语料库查询 """
        corpusbase = self.create_instances([
            {
                "name": "语料库05",
                "code": "corpusbase05"
            }
        ], "CorpusBase")[0]
        url = "{0}?{1}".format(reverse("corpus:corpusbase-list"),
                               "name={0}".format(corpusbase.name))

        response = self.client.get(url, **self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         response.content)
        self.assertEqual(1, len(response_data))
        self.assertEqual(corpusbase.name, response_data[0]["name"])

    def test_corpusbase_aoj_user_relations(self):
        """ 测试语料库与机构领域与用户与租户与关联关系"""
        aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]
        corpusbase = self.create_instances([
            {
                "name": "语料库06",
                "code": "corpusbase06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": aoj
            },
            {
                "name": "语料库07",
                "code": "corpusbase07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": aoj
            }
        ], "CorpusBase")

        # 测试语料库和租户间的关系
        self.assertEqual(corpusbase[0].tenant, corpusbase[1].tenant)
        self.assertEqual(corpusbase[0].tenant.name, self.tenants[0].name)
        # 测试语料库和用户间的关系
        self.assertEqual(corpusbase[0].owner, corpusbase[1].owner)
        self.assertEqual(corpusbase[0].owner.username, self.users[0].username)
        # 测试语料库和机构领域的关系
        self.assertEqual(corpusbase[0].area_of_job,
                         corpusbase[1].area_of_job)
        self.assertEqual(corpusbase[0].area_of_job.name, aoj.name)
        # 测试语料库中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(corpusbase[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)
