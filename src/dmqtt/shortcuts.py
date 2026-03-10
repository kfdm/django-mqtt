import uuid
from functools import lru_cache, wraps

from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from paho.mqtt import publish

from .decorators import json_payload

__all__ = [
    "default_client_id",
    "single",
]


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
