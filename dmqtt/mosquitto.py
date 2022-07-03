import json
import logging

from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import path

logger = logging.getLogger(__name__)


# https://github.com/iegomez/mosquitto-go-auth#http
class GetUser(APIView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        user = authenticate(
            request,
            username=data["username"],
            password=data["password"],
        )
        if user is None:
            return HttpResponseForbidden()

        user_logged_in.send(sender=user.__class__, request=request, user=user)

        return JsonResponse({"result": "ok"})


class ACLCheck(APIView):
    def post(self, request):
        # TODO Proper auth
        return JsonResponse({"result": "ok"})


urlpatterns = [
    path("getuser", GetUser.as_view()),
    path("aclcheck", ACLCheck.as_view()),
]
