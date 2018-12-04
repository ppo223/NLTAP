import json
import time

from django.urls import reverse
from rest_framework import status

from cwtap.core.test import CWTAPAPITestCase
from .models import ModelBase, Model, ModelInstance


class ModelBaseTest(CWTAPAPITestCase):
    """ 测试模型库表 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]

    def test_modelbase_create(self):
        """ 测试模型库创建 """
        url = reverse("algorithm_models:modelbase-list")
        data = {
            "name": "模型库01",
            "code": "modelbase01",
            "area_of_job": self.aoj.id
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

    def test_modelbase_delete(self):
        """ 测试模型库删除 """
        modelbases = self.create_instances([
            {
                "name": "模型库_02",
                "code": "modelbase_02",
                "area_of_job": self.aoj
            },
            {
                "name": "模型库_03",
                "code": "modelbase_03",
                "area_of_job": self.aoj
            }
        ], "ModelBase")

        url = reverse("algorithm_models:modelbase-detail",
                      args=(modelbases[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(ModelBase.objects.all()))
        self.assertEqual(modelbases[1].name,
                         ModelBase.objects.get(id=modelbases[1].id).name)

    def test_modelbase_update(self):
        """ 测试模型库修改 """
        modelbases = self.create_instances([
            {
                "name": "模型库_0401",
                "code": "modelbase_0401",
                "area_of_job": self.aoj
            },
            {
                "name": "模型库_0402",
                "code": "modelbase_0402",
                "area_of_job": self.aoj
            }
        ], "ModelBase")

        url = reverse("algorithm_models:modelbase-detail",
                      args=(modelbases[0].id,))

        data = {
            "name": "模型库_0401修改",
            "code": "modelbase_0401修改",
            "details": "你好，模型库_0401修改",
            "area_of_job": self.aoj.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"],
                         ModelBase.objects.get(id=modelbases[0].id).name)
        self.assertEqual(modelbases[1].name,
                         ModelBase.objects.get(id=modelbases[1].id).name)

    def test_modelbase_timeupdate(self):
        """ 测试模型库的时间修改 """
        modelbases = self.create_instances([
            {
                "name": "模型库_00",
                "code": "modelbase_00",
                "area_of_job": self.aoj
            }
        ], "ModelBase")[0]
        created, modified = modelbases.created, modelbases.modified
        time.sleep(1)
        modelbases.name = "模型库_00_修改"
        modelbases.save()

        self.assertEqual(modelbases.created, created)
        self.assertTrue(modelbases.modified > modified)

    def test_modelbase_query(self):
        """ 测试模型库查询 """
        modelbases = self.create_instances([
            {
                "name": "模型库_0501",
                "code": "modelbase_0501",
                "area_of_job": self.aoj
            },
            {
                "name": "模型库_0502",
                "code": "modelbase_0502",
                "area_of_job": self.aoj
            }
        ], "ModelBase")

        url = "{0}?{1}".format(reverse("algorithm_models:modelbase-list"),
                               "name=模型库_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modelbases[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("algorithm_models:modelbase-list"),
                               "name=模型库_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modelbases[1].name, query_result[0]["name"])

    def test_know_aoj_user_relations(self):
        """ 试模型库与用户与租户与机构领域关联关系 """
        modelbases = self.create_instances([
            {
                "name": "模型库06",
                "code": "modelbase06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": self.aoj
            },
            {
                "name": "模型库07",
                "code": "modelbase07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "area_of_job": self.aoj
            }
        ], "ModelBase")

        # 测试模型库和租户间的关系
        self.assertTrue(not None, self.tenants[0].name)
        self.assertEqual(modelbases[0].tenant, modelbases[1].tenant)
        self.assertEqual(modelbases[0].tenant.name, self.tenants[0].name)
        # 测试模型库和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(modelbases[0].owner, modelbases[1].owner)
        self.assertEqual(modelbases[0].owner.username, self.users[0].username)
        # 测试模型库和机构领域的关系
        self.assertTrue(not None, self.aoj.name)
        self.assertEqual(modelbases[0].area_of_job, modelbases[1].area_of_job)
        self.assertEqual(modelbases[0].area_of_job.name, self.aoj.name)
        # 测试模型库中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(modelbases[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)


class ModelTest(CWTAPAPITestCase):
    """ 测试模型表 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]

        self.modelbase = self.create_instances([
            {
                "name": "模型库_00",
                "code": "modelbase_00",
                "area_of_job": self.aoj
            }
        ], "ModelBase")[0]

    def test_model_create(self):
        """ 测试模型创建 """
        url = reverse("algorithm_models:model-list")
        data = {
            "name": "模型_01",
            "code": "model_01",
            "modelbase": self.modelbase.id
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

        response = self.client.get(url, **self.auth_header)
        self.assertEqual(data["name"],
                         json.loads(response.content)[0]["name"])

    def test_model_delete(self):
        """ 测试模型删除 """
        models = self.create_instances([
            {
                "name": "模型02",
                "code": "model02",
                "modelbase": self.modelbase
            },
            {
                "name": "模型03",
                "code": "model03",
                "modelbase": self.modelbase
            }
        ], "Model")

        url = reverse("algorithm_models:model-detail",
                      args=(models[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(Model.objects.all()))
        self.assertEqual(models[1].name,
                         Model.objects.get(id=models[1].id).name)

    def test_models_update(self):
        """ 测试模型修改 """
        models = self.create_instances([
            {
                "name": "模型_0401",
                "code": "model_0401",
                "modelbase": self.modelbase
            },
            {
                "name": "模型_0402",
                "code": "model_0402",
                "modelbase": self.modelbase
            }
        ], "Model")

        url = reverse("algorithm_models:model-detail", args=(models[1].id,))
        data = {
            "name": "模型_0402修改",
            "code": "model_0402修改",
            "modelbase": self.modelbase.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models[0].name,
                         Model.objects.get(id=models[0].id).name)
        self.assertEqual(data["name"],
                         Model.objects.get(id=models[1].id).name)

    def test_models_timeupdate(self):
        """ 测试模型时间修改 """
        models = self.create_instances([
            {
                "name": "模型_00",
                "code": "model_00",
                "modelbase": self.modelbase
            }
        ], "Model")[0]

        created, modified = models.created, models.modified

        time.sleep(1)
        models.name = "模型_00_修改"
        models.save()

        self.assertEqual(models.created, created)
        self.assertTrue(models.modified > modified)

    def test_models_query(self):
        """ 测试查询模型 """
        models = self.create_instances([
            {
                "name": "模型_0501",
                "code": "model_0501",
                "modelbase": self.modelbase
            },
            {
                "name": "模型_0502",
                "code": "model_0502",
                "modelbase": self.modelbase
            }
        ], "Model")

        url = "{0}?{1}".format(reverse("algorithm_models:model-list"),
                               "name=模型_0501")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("algorithm_models:model-list"),
                               "name=模型_0502")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models[1].name, query_result[0]["name"])

    def test_model_aoj_user_relations(self):
        """ 测试模型与机构领域与用户与租户关联关系 """
        models = self.create_instances([
            {
                "name": "模型06",
                "code": "model06",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "modelbase": self.modelbase
            },
            {
                "name": "模型07",
                "code": "model07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "modelbase": self.modelbase
            }
        ], "Model")

        # 测试模型和租户间的关系
        self.assertTrue(not None, self.tenants[0].name)
        self.assertEqual(models[0].tenant, models[1].tenant)
        self.assertEqual(models[0].tenant.name, self.tenants[0].name)
        # 测试模型和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(models[0].owner, models[1].owner)
        self.assertEqual(models[0].owner.username, self.users[0].username)
        # 测试模型和模型库的关系
        self.assertTrue(not None, self.modelbase.name)
        self.assertEqual(models[0].modelbase, models[1].modelbase)
        self.assertEqual(models[0].modelbase.name, self.modelbase.name)
        # 测试模型中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(models[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)


class ModelInstanceTest(CWTAPAPITestCase):
    """ 模型实例测试类 """

    def setUp(self):
        super().setUp()
        self.aoj = self.create_instances([
            {
                "name": "机构01",
                "owner": self.users[0],
                "tenant": self.tenants[0]
            }
        ], "AreaOfJob")[0]
        self.modelbase = self.create_instances([
            {
                "name": "模型库_00",
                "code": "modelbase_00",
                "area_of_job": self.aoj
            }
        ], "ModelBase")[0]

        self.model = self.create_instances([
            {
                "name": "模型01",
                "modelbase": self.modelbase
            }
        ], "Model")[0]

    def test_modelinstance_create(self):
        """ 测试模型实例创建 """
        url = reverse("algorithm_models:modelinstance-list")
        data = {
            "name": "实例_00",
            "uuid": "实例号_00",
            "model": self.model.id
        }
        response = self.client.post(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["name"], json.loads(response.content)["name"])

        response = self.client.get(url, **self.auth_header)
        self.assertEqual(data["name"],
                         json.loads(response.content)[0]["name"])

    def test_modelinstance_delete(self):
        """ 测试实例删除 """
        modelinstances = self.create_instances([
            {
                "name": "实例02",
                "uuid": "实例号_02",
                "model": self.model
            },
            {
                "name": "实例03",
                "uuid": "实例号_03",
                "model": self.model
            }
        ], "ModelInstance")

        url = reverse("algorithm_models:modelinstance-detail",
                      args=(modelinstances[0].id,))
        response = self.client.delete(url, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, len(ModelInstance.objects.all()))
        self.assertEqual(modelinstances[1].name,
                         ModelInstance.objects.get(
                             id=modelinstances[1].id).name)

    def test_modelsinstance_update(self):
        """ 测试实例修改 """
        modelinstances = self.create_instances([
            {
                "name": "实例_0401",
                "uuid": "实例号_0401",
                "model": self.model
            },
            {
                "name": "实例_0402",
                "uuid": "实例号_0402",
                "model": self.model
            }
        ], "ModelInstance")

        url = reverse("algorithm_models:modelinstance-detail",
                      args=(modelinstances[1].id,))
        data = {
            "name": "实例_0402修改",
            "uuid": "实例号_0402修改",
            "model": self.model.id
        }
        response = self.client.put(url, data, **self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modelinstances[0].name,
                         ModelInstance.objects.get(
                             id=modelinstances[0].id).name)
        self.assertEqual(data["name"],
                         ModelInstance.objects.get(
                             id=modelinstances[1].id).name)

    def test_modelinstance_timeupdate(self):
        """ 测试实例时间修改 """
        modelinstances = self.create_instances([
            {
                "name": "实例05",
                "uuid": "实例号05",
                "model": self.model
            }
        ], "ModelInstance")[0]

        created, modified = modelinstances.created, modelinstances.modified
        time.sleep(1)
        modelinstances.name = "模型05_修改"
        modelinstances.save()

        self.assertEqual(modelinstances.created, created)
        self.assertTrue(modelinstances.modified > modified)

    def test_modelinstance_query(self):
        """ 测试实例查询 """
        modelinstances = self.create_instances([
            {
                "name": "实例_0601",
                "uuid": "实例号_0601",
                "model": self.model
            },
            {
                "name": "实例_0602",
                "uuid": "实例号_0602",
                "model": self.model
            }
        ], "ModelInstance")

        url = "{0}?{1}".format(reverse("algorithm_models:modelinstance-list"),
                               "name=实例_0601")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modelinstances[0].name, query_result[0]["name"])

        url = "{0}?{1}".format(reverse("algorithm_models:modelinstance-list"),
                               "name=实例_0602")
        response = self.client.get(url, **self.auth_header)
        query_result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(modelinstances[1].name, query_result[0]["name"])

    def test_modelinstance_model_user_relations(self):
        """ 测试实例与模型与用户与租户间关系 """
        modelinstances = self.create_instances([
            {
                "name": "实例07",
                "uuid": "实例号07",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "model": self.model
            },
            {
                "name": "实例08",
                "uuid": "实例号08",
                "owner": self.users[0],
                "tenant": self.tenants[0],
                "model": self.model
            }
        ], "ModelInstance")

        # 测试实例和租户间的关系
        self.assertTrue(not None, self.tenants[0].name)
        self.assertEqual(modelinstances[0].tenant, modelinstances[1].tenant)
        self.assertEqual(modelinstances[0].tenant.name, self.tenants[0].name)
        # 测试实例和用户间的关系
        self.assertTrue(not None, self.users[0].username)
        self.assertEqual(modelinstances[0].owner, modelinstances[1].owner)
        self.assertEqual(modelinstances[0].owner.username,
                         self.users[0].username)
        # 测试实例和模型的关系
        self.assertTrue(not None, self.model.name)
        self.assertEqual(modelinstances[0].model, modelinstances[1].model)
        self.assertEqual(modelinstances[0].model.name, self.model.name)
        # 测试实例中租户和用户间的关系
        self.assertEqual(self.tenants[0].name,
                         self.users[0].userprofile.tenant.name)
        self.assertEqual(modelinstances[1].owner.userprofile.tenant.name,
                         self.tenants[0].name)
