import base64

from django.conf import settings
from django.apps import apps
from oauth2_provider.models import get_application_model


class Utils(object):
    """工具类"""

    @staticmethod
    def reverse_model(model):
        arr_model = str(model._meta).split(".")
        return (arr_model[-1], arr_model[0])

    @staticmethod
    def get_model_app_relations():
        return dict(map(Utils.reverse_model, apps.get_models()))

    @staticmethod
    def init_password_grant_application(client_id=settings.CLIENT_ID,
                                        client_secret=settings.CLIENT_SECRET):
        Application = get_application_model()
        apps = Application.objects.filter(
            authorization_grant_type=Application.GRANT_PASSWORD)
        if len(apps) == 0:
            app = Application(
                name="Test Application",
                client_id=client_id,
                client_secret=client_secret,
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_PASSWORD,
            )
            app.save()
        else:
            app = apps[0]

        return app

    @staticmethod
    def get_basic_auth_header(user, password):
        user_pass = "{0}:{1}".format(user, password)
        auth_string = base64.b64encode(user_pass.encode("utf-8"))
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic {0}".format(
                auth_string.decode("utf-8")),
        }

        return auth_headers

    @staticmethod
    def get_auth_header(access_token):
        return {"HTTP_AUTHORIZATION": "Bearer {0}".format(access_token)}
