import json
import time

from django.urls import reverse
from rest_framework import status
from cwtap.core.test import CWTAPAPITestCase

from .models import RuleBase, Rule


class RuleBaseTest(CWTAPAPITestCase):
    """ 测试规则库 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]

    def test_rulebase_create(self):
        """ 测试规则库创建 """
        url = reverse("rules:rulebase-list")
        data = {
            "name": "规则库01",
            "code": "rulebase01",
            "area_of_job": self.aoj.id
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

    def test_rulebase_delete(self):
        """ 测试规则库删除 """
        rulebases = self.create_instances([
            {
                "name": "规则库_02",
                "code": "rulebase_02",
                "area_of_job": self.aoj
            },
            {
                "name": "规则库_03",
                "code": "rulebase_03",
                "area_of_job": self.aoj
            }
        ], "RuleBase")
        url = reverse("rules:rulebase-detail",
                      args=(rulebases[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(RuleBase.objects.all()))
        self.assertEqual(rulebases[1].name,
                         RuleBase.objects.get(id=rulebases[1].id).name)

    def test_rulebase_update(self):
        """ 测试规则库修改 """
        rulebases = self.create_instances([
            {
                "name": "规则库_0401",
                "code": "rulebase_0401",
                "area_of_job": self.aoj
            },
            {
                "name": "规则库_0402",
                "code": "rulebase_0402",
                "area_of_job": self.aoj
            }
        ], "RuleBase")

        url = reverse("rules:rulebase-detail", args=(rulebases[0].id,))
        data = {
            "name": "规则库_0401修改",
            "code": "rulebase_0401修改",
            "details": "你好，规则库_0401修改",
            "area_of_job": self.aoj.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"],
                         RuleBase.objects.get(id=rulebases[0].id).name)
        self.assertEqual(rulebases[1].name,
                         RuleBase.objects.get(id=rulebases[1].id).name)

    def test_rulebase_timeupdate(self):
        """ 测试规则库的时间修改 """
        rulebases = self.create_instances([
            {
                "name": "规则库_00",
                "code": "rulebase_00",
                "area_of_job": self.aoj
            }
        ], "RuleBase")[0]

        created, modified = rulebases.created, rulebases.modified
        time.sleep(1)
        rulebases.name = "规则库_00_修改"
        rulebases.save()

        self.assertEqual(rulebases.created, created)
        self.assertTrue(rulebases.modified > modified)

    def test_rulebase_query(self):
        """ 测试规则库查询 """
        rulebases = self.create_instances([
            {
                "name": "规则库_0501",
                "code": "rulebase_0501",
                "area_of_job": self.aoj
            },
            {
                "name": "规则库_0502",
                "code": "rulebase_0502",
                "area_of_job": self.aoj
            }
        ], "RuleBase")

        url = "{0}?{1}".format(reverse("rules:rulebase-list"),
                               "name=规则库_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rulebases[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("rules:rulebase-list"),
                               "name=规则库_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rulebases[1].name, query_result[0]["name"])

    def test_know_aoj_user_relations(self):
        """ 测试规则库与用户与租户与机构领域关联关系 """
        rulebases = self.create_instances([
            {
                "name": "规则库06",
                "code": "rulebase06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": self.aoj
            },
            {
                "name": "规则库07",
                "code": "rulebase07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": self.aoj
            }
        ], "RuleBase")

        # 测试规则库和租户间的关系
        self.assertTrue(not None, rulebases[1].tenant.name)
        self.assertEqual(rulebases[0].tenant, rulebases[1].tenant)
        self.assertEqual(rulebases[0].tenant.name, self.tenants[0].name)
        # 测试规则库和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(rulebases[0].owner, rulebases[1].owner)
        self.assertEqual(rulebases[0].owner.username, self.users[0].username)
        # 测试规则库和机构领域的关系
        self.assertTrue(not None, self.aoj.name)
        self.assertEqual(rulebases[0].area_of_job, rulebases[1].area_of_job)
        self.assertEqual(rulebases[0].area_of_job.name, self.aoj.name)
        # 测试规则库中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(rulebases[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)


class RuleTest(CWTAPAPITestCase):
    """ 测试规则表 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([{"name": "机构_00"}], "AreaOfJob")[0]

        self.labelbase = self.create_instances([
            {"name": "标签库_00", "area_of_job": self.aoj}], "LabelBase")[0]

        self.label = self.create_instances([
            {"name": "标签_00", "labelbase": self.labelbase}], "Label")[0]

        self.rulebase = self.create_instances([
            {"name": "规则库01", "area_of_job": self.aoj}], "RuleBase")[0]

    def test_rule_create(self):
        """ 测试规则创建 """
        url = reverse("rules:rule-list")
        data = {"label": self.label.id, "rulebase": self.rulebase.id}
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["label"],
                         json.loads(response.content)["label"])

    def test_rule_delete(self):
        """ 测试规则删除 """
        rules = self.create_instances([
            {
                "originate_object": "规则来源_01",
                "label": self.label,
                "rulebase": self.rulebase
            },
            {
                "originate_object": "规则来源_02",
                "label": self.label,
                "rulebase": self.rulebase
            }
        ], "Rule")

        url = reverse("rules:rule-detail", args=(rules[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(Rule.objects.all()))
        self.assertEqual(rules[1].originate_object,
                         Rule.objects.get(id=rules[1].id).originate_object)

    def test_rule_update(self):
        """ 测试规则修改 """
        rules = self.create_instances([
            {
                "originate_object": "规则来源_0301",
                "label": self.label,
                "rulebase": self.rulebase
            },
            {
                "originate_object": "规则来源_0302",
                "label": self.label,
                "rulebase": self.rulebase
            }
        ], "Rule")

        url = reverse("rules:rule-detail", args=(rules[0].id,))
        data = {
            "originate_object": "规则来源_0301修改",
            "label": self.label.id,
            "rulebase": self.rulebase.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["originate_object"],
                         Rule.objects.get(id=rules[0].id).originate_object)
        self.assertEqual(rules[1].originate_object,
                         Rule.objects.get(id=rules[1].id).originate_object)

    def test_rule_timeupdate(self):
        """ 测试规则的时间修改 """
        rules = self.create_instances([
            {
                "originate_object": "规则来源_04",
                "label": self.label,
                "rulebase": self.rulebase
            }
        ], "Rule")[0]

        created, modified = rules.created, rules.modified

        time.sleep(1)
        rules.originate_object = "规则来源_04_修改"
        rules.save()

        self.assertEqual(rules.created, created)
        self.assertTrue(rules.modified > modified)

    def test_rule_query(self):
        """ 测试规则查询 """
        rules = self.create_instances([
            {
                "originate_object": "规则来源_0501",
                "label": self.label,
                "rulebase": self.rulebase
            },
            {
                "originate_object": "规则来源_0502",
                "label": self.label,
                "rulebase": self.rulebase
            }
        ], "Rule")

        url = "{0}?{1}".format(reverse("rules:rule-list"),
                               "originate_object=规则来源_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rules[0].originate_object,
                         query_result[0]["originate_object"])

        url = "{0}?{1}".format(reverse("rules:rule-list"),
                               "originate_object=规则来源_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rules[1].originate_object,
                         query_result[0]["originate_object"])

    def test_rule_user_relations(self):
        """ 测试规则与用户与租户与规则库关联关系 """
        rules = self.create_instances([
            {
                "originate_object": "规则来源_06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "label": self.label,
                "rulebase": self.rulebase
            },
            {
                "originate_object": "规则来源_07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "label": self.label,
                "rulebase": self.rulebase
            }
        ], "Rule")

        # 测试规则和租户间的关系
        self.assertTrue(not None, rules[1].tenant.name)
        self.assertEqual(rules[0].tenant, rules[1].tenant)
        self.assertEqual(rules[0].tenant.name, self.tenants[0].name)
        # 测试规则和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(rules[0].owner, rules[1].owner)
        self.assertEqual(rules[0].owner.username, self.users[0].username)
        # 测试规则和规则库的关系
        self.assertTrue(not None, self.rulebase.name)
        self.assertEqual(rules[0].rulebase, rules[1].rulebase)
        self.assertEqual(rules[0].rulebase.name, self.rulebase.name)
        # 测试规则中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(rules[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)
