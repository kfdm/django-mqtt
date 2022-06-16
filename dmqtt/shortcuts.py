import json
import uuid
from functools import lru_cache

from paho.mqtt import publish

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

# The JSONEncoder from DRF handles quite a few types, so we efault to that
# if avaiable and if not fallback to the Django one which still handles some
# extra types
try:
    from rest_framework.utils.encoders import JSONEncoder
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder


__all__ = ["single"]


@lru_cache(maxsize=1)
def client_id():
    return (get_current_site(None).domain + "-%d" % uuid.uuid4().int)[:32]


def single(topic, **kwargs):
    if "json" in kwargs:
        data = kwargs.pop("json")
        kwargs["payload"] = json.dumps(data, cls=JSONEncoder).encode("utf8")

    if settings.MQTT_USER and settings.MQTT_PASS:
        kwargs["auth"] = {
            "username": settings.MQTT_USER,
            "password": settings.MQTT_PASS,
        }

    return publish.single(
        topic,
        client_id=client_id(),
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
        **kwargs,
    )
