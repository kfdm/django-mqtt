import json
import uuid
from functools import lru_cache, wraps
from django.apps import apps
from paho.mqtt import publish

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

# The JSONEncoder from DRF handles quite a few types, so we default to that
# if available and if not fallback to the Django one which still handles some
# extra types
try:
    from rest_framework.utils.encoders import JSONEncoder
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder


__all__ = ["single", "json_payload"]


def json_payload(func):
    """
    Decorator to add json support to MQTT publish methods
    """

    @wraps(func)
    def __inner(*args, **kwargs):
        if "json" in kwargs:
            data = kwargs.pop("json")
            kwargs["payload"] = json.dumps(data, cls=JSONEncoder).encode("utf8")

        return func(*args, **kwargs)

    return __inner


@lru_cache(maxsize=1)
def default_client_id():
    if apps.is_installed("django.contrib.sites"):
        return (get_current_site(None).domain + "-%d" % uuid.uuid4().int)[:32]
    return ""


@json_payload
@wraps(publish.single)
def single(topic, client_id=None, **kwargs):
    """
    Wrapped version of single, supporting AUTH and json payload
    """
    if settings.MQTT_USER and settings.MQTT_PASS:
        kwargs["auth"] = {
            "username": settings.MQTT_USER,
            "password": settings.MQTT_PASS,
        }
    if client_id is None:
        client_id = default_client_id()

    return publish.single(
        topic,
        client_id=client_id,
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
        **kwargs,
    )
