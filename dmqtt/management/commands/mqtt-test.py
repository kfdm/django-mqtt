import sys

from paho.mqtt.publish import single

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        mqtt = parser.add_argument_group("mqtt server arguments")
        mqtt.add_argument("topic", help="MQTT Topic to send to")
        mqtt.add_argument("-u", "--user", default=settings.MQTT_USER)
        mqtt.add_argument("-P", "--password", default=settings.MQTT_PASS)
        mqtt.add_argument("-H", "--host", default=settings.MQTT_HOST)
        mqtt.add_argument("--port", default=settings.MQTT_PORT, type=int)

    def handle(self, topic, **kwargs):
        single(
            topic=topic,
            payload=sys.stdin.read().encode("utf8"),
            client_id="test",
            hostname=kwargs["host"],
            port=int(kwargs["port"]),
            auth={"username": kwargs["user"], "password": kwargs["password"]},
        )
