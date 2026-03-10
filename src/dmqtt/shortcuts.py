import uuid
import typing
from functools import lru_cache, wraps

from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from paho.mqtt import publish
from .decorators import json_payload


if typing.TYPE_CHECKING:
    from paho.mqtt.client import PayloadType


__all__ = [
    "default_client_id",
    "multiple",
    "single",
]


@lru_cache(maxsize=1)
def default_client_id():
    if apps.is_installed("django.contrib.sites"):
        return (get_current_site(None).domain + "-%d" % uuid.uuid4().int)[:32]
    return ""


@wraps(publish.multiple)
def multiple(msgs: "publish.MessagesList", client_id=None, **kwargs):
    if settings.MQTT_USER and settings.MQTT_PASS:
        kwargs["auth"] = {
            "username": settings.MQTT_USER,
            "password": settings.MQTT_PASS,
        }
    if client_id is None:
        client_id = default_client_id()
    return publish.multiple(
        msgs,
        hostname=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
        client_id=client_id,
        **kwargs,
    )


@json_payload
@wraps(publish.single)
def single(
    topic: str,
    payload: "PayloadType" = None,
    qos: int = 0,
    retain: bool = False,
    **kwargs,
) -> None:
    """
    Wrapped version of single, supporting AUTH and json payload
    """
    msg: "publish.MessageDict" = {
        "topic": topic,
        "payload": payload,
        "qos": qos,
        "retain": retain,
    }
    return multiple([msg], **kwargs)
