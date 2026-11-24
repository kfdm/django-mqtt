import sys

from django.core.management.base import BaseCommand, CommandParser
from paho.mqtt.publish import single

from . import ClientMixin, LoggingMixin


class Command(ClientMixin, LoggingMixin, BaseCommand):
    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)
        mqtt = parser.add_argument_group("message arguments")
        mqtt.add_argument("topic", help="MQTT Topic to send to")
        mqtt.add_argument("--qos", default=0, type=int)
        mqtt.add_argument("--retain", action="store_true")

    def handle(self, topic, **options):
        payload = sys.stdin.read().strip().encode("utf8")

        kwargs = self.client_arguments(options)
        if auth := self.auth_arguments(options):
            kwargs["auth"] = auth

        single(
            topic=topic,
            payload=payload,
            **kwargs,
        )
