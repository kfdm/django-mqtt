import json
import logging

from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden, JsonResponse

logger = logging.getLogger(__name__)


# https://docs.vernemq.com/plugindevelopment/webhookplugins#auth_on_register
class Auth(APIView):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if authenticate(request, username=data["username"], password=data["password"]):
            return JsonResponse({"result": "ok"})
        logger.error("Invalid login for %s", data["username"])
        return HttpResponseForbidden()
