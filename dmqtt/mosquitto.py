import json
import logging

from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import path
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


# https://github.com/iegomez/mosquitto-go-auth#http
class GetUser(APIView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if authenticate(request, username=data["username"], password=data["password"]):
            return JsonResponse({"result": "ok"})
        logger.debug("Invalid login for %s", data["username"])
        return HttpResponseForbidden()


class ACLCheck(APIView):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


urlpatterns = [
    path("getuser", GetUser.as_view()),
    path("aclcheck", ACLCheck.as_view()),
]
