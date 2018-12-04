import sys

from django.test import TestCase
from django.urls import reverse
from django.apps import apps
from rest_framework import status

from cwtap.core.test import CWTAPAPITestCase
from cwtap.core.utils import Utils
from users.models import Tenant


class UtilsTest(TestCase):

    def test_get_model_app_relations(self):
        relations = Utils.get_model_app_relations()

        self.assertEqual("users", relations["userprofile"])
        self.assertEqual("users", relations["tenant"])

    def test_get_model(self):
        relations = Utils.get_model_app_relations()

        self.assertEqual(Tenant, apps.get_model(relations["tenant"], "tenant"))


class CWTAPAPITestCaseTest(CWTAPAPITestCase):

    def test_api(self):
        response = self.client.get(
            reverse("management:user-list"), **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PythonEnvTest(TestCase):

    def test_python_version(self):
        """ 测试执行 python 版本 """
        self.assertTrue(sys.version.startswith("3"))


class PythonGrammarTest(TestCase):

    variable_01 = "variable_01_value"

    def test_class_variable(self):
        """ 测试类变量 """
        self.assertEqual("variable_01_value", self.variable_01)
        self.assertTrue(self.variable_01 is not None)

    def test_list_none(self):
        """ 测试 python 列表为空 """
        self.assertEqual(0, len([]))

    def test_judge_list_type(self):
        """ 判断列表类型 """
        self.assertTrue(isinstance([], list))

    def test_string_is_none(self):
        """ 测试字符串是否为空 """
        self.assertTrue(not "   ".strip())
