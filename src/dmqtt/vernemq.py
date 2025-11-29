import json
import logging

from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_login_failed
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import path
from django.views import View
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_register
class OnRegister(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if authenticate(request, username=data["username"], password=data["password"]):
            return JsonResponse({"result": "ok"})
        logger.debug("Invalid login for %s", data["username"])
        user_login_failed.send(
            sender=__name__,
            credentials={key: data[key] for key in data if key not in ["password"]},
            request=request,
        )
        return HttpResponseForbidden()


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_subscribe
class OnSubscribe(View):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_publish
class OnPublish(View):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


urlpatterns = [
    path("auth_on_register", csrf_exempt(OnRegister.as_view())),
    path("auth_on_subscribe", csrf_exempt(OnSubscribe.as_view())),
    path("auth_on_publish", csrf_exempt(OnPublish.as_view())),
]
