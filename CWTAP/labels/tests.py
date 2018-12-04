import json
import time

from django.urls import reverse
from rest_framework import status

from cwtap.core.test import CWTAPAPITestCase
from .models import LabelBase, Label


class LabelBaseTest(CWTAPAPITestCase):
    """ 测试标签库 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]

    def test_labelbase_create(self):
        """ 测试标签库创建 """
        url = reverse("labels:labelbase-list")
        data = {"name": "标签库00", "code": "labelbase00"}
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(["This field is required."],
                         json.loads(response.content)["area_of_job"])

        data = {
            "name": "标签库01",
            "code": "labelbase01",
            "area_of_job": self.aoj.id
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

        response = self.client.get(url, **self.auth_header)
        self.assertEqual(data["name"],
                         json.loads(response.content)[0]["name"])

    def test_labelbase_delete(self):
        """ 测试标签库删除 """
        labelbases = self.create_instances([
            {
                "name": "标签库02",
                "code": "labelbase02",
                "area_of_job": self.aoj
            },
            {
                "name": "标签库03",
                "code": "labelbase03",
                "area_of_job": self.aoj
            }
        ], "LabelBase")

        url = reverse("labels:labelbase-detail",
                      args=(labelbases[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(LabelBase.objects.all()))
        self.assertEqual(labelbases[1].name,
                         LabelBase.objects.get(id=labelbases[1].id).name)

    def test_labelbase_update(self):
        """ 测试标签库修改 """
        labelbases = self.create_instances([
            {
                "name": "标签库_0401",
                "code": "labelbase_0401",
                "area_of_job": self.aoj
            },
            {
                "name": "标签库_0402",
                "code": "labelbase_0402",
                "area_of_job": self.aoj
            }
        ], "LabelBase")

        url = reverse("labels:labelbase-detail",
                      args=(labelbases[1].id,))
        data = {
            "name": "标签库_0402修改",
            "code": "labelbase_0402修改",
            "area_of_job": self.aoj.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(labelbases[0].name,
                         LabelBase.objects.get(id=labelbases[0].id).name)
        self.assertEqual(data["name"],
                         LabelBase.objects.get(id=labelbases[1].id).name)

    def test_labelbase_timeupdate(self):
        """ 测试标签库时间修改 """
        labelbases = self.create_instances([
            {
                "name": "标签库_00",
                "code": "labelbase_00",
                "area_of_job": self.aoj
            }
        ], "LabelBase")[0]
        created, modified = labelbases.created, labelbases.modified

        time.sleep(1)
        labelbases.name = "标签库_00_修改"
        labelbases.save()

        self.assertEqual(labelbases.created, created)
        self.assertTrue(labelbases.modified > modified)

    def test_labelbase_query(self):
        """ 测试标签库查询 """
        labelbases = self.create_instances([
            {
                "name": "标签库_0501",
                "code": "labelbase_0501",
                "area_of_job": self.aoj
            },
            {
                "name": "标签库_0502",
                "code": "labelbase_0502",
                "area_of_job": self.aoj
            }
        ], "LabelBase")

        url = "{0}?{1}".format(reverse("labels:labelbase-list"),
                               "name=标签库_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(labelbases[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("labels:labelbase-list"),
                               "name=标签库_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(labelbases[1].name, query_result[0]["name"])

    def test_label_aoj_user_relations(self):
        """ 测试标签库与机构领域与用户与租户与关联关系"""
        labelbases = self.create_instances([
            {
                "name": "标签库06",
                "code": "labelbase06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": self.aoj
            },
            {
                "name": "标签库07",
                "code": "labelbase07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": self.aoj
            }
        ], "LabelBase")

        # 测试标签库和租户间的关系
        self.assertTrue(not None, self.tenants[0].name)
        self.assertEqual(labelbases[0].tenant, labelbases[1].tenant)
        self.assertEqual(labelbases[0].tenant.name, self.tenants[0].name)
        # 测试标签库和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(labelbases[0].owner, labelbases[1].owner)
        self.assertEqual(labelbases[0].owner.username, self.users[0].username)
        # 测试标签库和机构领域的关系
        self.assertTrue(not None, self.aoj.name)
        self.assertEqual(labelbases[0].area_of_job, labelbases[1].area_of_job)
        self.assertEqual(labelbases[0].area_of_job.name, self.aoj.name)
        # 测试标签库中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(labelbases[1].owner.userprofile.tenant.name,
                         self.users[0].userprofile.tenant.name)


class LabelTest(CWTAPAPITestCase):
    """ 测试标签表 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]

        self.labelbase = self.create_instances([
            {
                "name": "标签库_00",
                "code": "labelbase_00",
                "area_of_job": self.aoj
            }
        ], "LabelBase")[0]

    def test_label_create(self):
        """ 测试标签创建 """
        url = reverse("labels:label-list")

        data = {
            # "name": "标签_00",
            "code": "label_00",
            "labelbase": self.labelbase
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(["This field is required."],
                         json.loads(response.content)["name"])

        data = {
            "name": "标签_01",
            "code": "label_01",
            "labelbase": self.labelbase.id
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

        response = self.client.get(url, **self.auth_header)
        self.assertEqual(data["name"],
                         json.loads(response.content)[0]["name"])

    def test_label_delete(self):
        """ 测试标签删除 """
        labels = self.create_instances([
            {
                "name": "标签02",
                "code": "label02",
                "labelbase": self.labelbase
            },
            {
                "name": "标签03",
                "code": "label03",
                "labelbase": self.labelbase
            }
        ], "Label")

        url = reverse("labels:label-detail",
                      args=(labels[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(1, len(Label.objects.all()))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(labels[1].name,
                         Label.objects.get(id=labels[1].id).name)

    def test_label_update(self):
        """ 测试标签修改 """
        labels = self.create_instances([
            {
                "name": "标签_0401",
                "code": "label_0401",
                "labelbase": self.labelbase
            },
            {
                "name": "标签_0402",
                "code": "label_0402",
                "labelbase": self.labelbase
            }
        ], "Label")

        url = reverse("labels:label-detail",
                      args=(labels[1].id,))
        data = {
            "name": "标签_0402修改",
            "code": "label_0402修改",
            "labelbase": self.labelbase.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(labels[0].name,
                         Label.objects.get(id=labels[0].id).name)
        self.assertEqual(data["name"],
                         Label.objects.get(id=labels[1].id).name)

    def test_label_query(self):
        """ 测试标签查询 """
        labels = self.create_instances([
            {
                "name": "标签_0501",
                "code": "label_0501",
                "labelbase": self.labelbase
            },
            {
                "name": "标签_0502",
                "code": "label_0502",
                "labelbase": self.labelbase
            }
        ], "Label")

        url = "{0}?{1}".format(reverse("labels:label-list"), "name=标签_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(labels[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("labels:label-list"), "name=标签_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(labels[1].name, query_result[0]["name"])

    def test_label_timeupdate(self):
        """ 测试标签的时间修改 """
        label = self.create_instances([
            {
                "name": "标签06",
                "code": "label06",
                "labelbase": self.labelbase
            }
        ], "Label")[0]

        created, modified = label.created, label.modified

        time.sleep(1)
        label.name = "标签06_修改"
        label.save()

        self.assertEqual(label.created, created)
        self.assertTrue(label.modified > modified)

    def test_label_labels_user_relations(self):
        """ 测试标签与标签库用户与租户关联关系 """
        labels = self.create_instances([
            {
                "name": "标签07",
                "code": "label07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "labelbase": self.labelbase
            },
            {
                "name": "标签08",
                "code": "label08",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "labelbase": self.labelbase
            }
        ], "Label")

        # 测试标签和租户间的关系
        self.assertTrue(not None, self.tenants[0].name)
        self.assertEqual(labels[0].tenant, labels[1].tenant)
        self.assertEqual(labels[0].tenant.name, self.tenants[0].name)
        # 测试标签和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(labels[0].owner, labels[1].owner)
        self.assertEqual(labels[1].owner.username, self.users[0].username)
        # 测试标签和标签库的关系
        self.assertTrue(not None, self.labelbase.name)
        self.assertEqual(labels[0].labelbase, labels[1].labelbase)
        self.assertEqual(labels[0].labelbase.name, self.labelbase.name)
        # 测试标签中租户和用户间的关系
        self.assertTrue(not None, self.users[0].userprofile.tenant.name)
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(labels[1].owner.userprofile.tenant.name,
                         self.users[0].userprofile.tenant.name)
        # 测试标签和机构领域间的关系
        self.assertEqual("机构01", labels[0].labelbase.area_of_job.name)
        self.assertEqual(labels[0].labelbase.area_of_job,
                         self.labelbase.area_of_job)
