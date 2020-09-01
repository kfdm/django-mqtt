import json
import logging

from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import path

logger = logging.getLogger(__name__)


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_register
class OnRegister(APIView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if authenticate(request, username=data["username"], password=data["password"]):
            return JsonResponse({"result": "ok"})
        logger.debug("Invalid login for %s", data["username"])
        return HttpResponseForbidden()


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_subscribe
class OnSubscribe(APIView):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_publish
class OnPublish(APIView):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


urlpatterns = [
    path("auth_on_register", OnRegister.as_view()),
    path("auth_on_subscribe", OnSubscribe.as_view()),
    path("auth_on_publish", OnPublish.as_view()),
]
