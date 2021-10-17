import json
import uuid
from functools import lru_cache

from paho.mqtt import publish
from rest_framework.utils.encoders import JSONEncoder

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

__all__ = ["single"]


@lru_cache(maxsize=1)
def client_id():
    return (get_current_site(None).domain + "-%d" % uuid.uuid4().int)[:32]


def single(topic, **kwargs):
    if "json" in kwargs:
        data = kwargs.pop("json")
        kwargs["payload"] = json.dumps(data, cls=JSONEncoder).encode("utf8")

    return publish.single(
        topic,
        client_id=client_id(),
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
        auth={"username": settings.MQTT_USER, "password": settings.MQTT_PASS},
        **kwargs
    )
