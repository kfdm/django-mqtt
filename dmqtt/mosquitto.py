import json
import logging

from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_login_failed
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import path

logger = logging.getLogger(__name__)


# https://github.com/iegomez/mosquitto-go-auth#http
class GetUser(APIView):
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


class ACLCheck(APIView):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


urlpatterns = [
    path("getuser", GetUser.as_view()),
    path("aclcheck", ACLCheck.as_view()),
]
