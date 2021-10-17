import sys

from paho.mqtt.publish import single

from django.conf import settings
from django.core.management.base import BaseCommand

from dmqtt.shortcuts import client_id


class Command(BaseCommand):
    def add_arguments(self, parser):
        mqtt = parser.add_argument_group("mqtt server arguments")
        mqtt.add_argument("topic", help="MQTT Topic to send to")
        mqtt.add_argument("-u", "--user", default=settings.MQTT_USER)
        mqtt.add_argument("-P", "--password", default=settings.MQTT_PASS)
        mqtt.add_argument("-H", "--host", default=settings.MQTT_HOST)
        mqtt.add_argument("--client-id", default=client_id())
        mqtt.add_argument("--port", default=settings.MQTT_PORT, type=int)
        mqtt.add_argument("--qos", default=0, type=int)
        mqtt.add_argument("--retain", action="store_true")

    def handle(self, topic, **kwargs):
        payload = sys.stdin.read().strip().encode("utf8")

        single(
            topic=topic,
            payload=payload,
            qos=kwargs["qos"],
            retain=kwargs["retain"],
            client_id=kwargs["client_id"],
            hostname=kwargs["host"],
            port=kwargs["port"],
            auth={"username": kwargs["user"], "password": kwargs["password"]},
        )
