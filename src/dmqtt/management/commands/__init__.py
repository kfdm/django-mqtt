import logging

from django.conf import settings
from django.core.management.base import CommandParser

from dmqtt.shortcuts import default_client_id


class ClientMixin:
    def add_arguments(self, parser: CommandParser):
        mqtt = parser.add_argument_group("mqtt connection arguments")
        mqtt.add_argument("-u", "--username", default=settings.MQTT_USER)
        mqtt.add_argument("-P", "--password", default=settings.MQTT_PASS)
        mqtt.add_argument("-H", "--host", default=settings.MQTT_HOST)
        mqtt.add_argument("--port", default=settings.MQTT_PORT, type=int)
        mqtt.add_argument("--client-id", default=default_client_id())

    def auth_arguments(self, options) -> dict:
        auth = {}
        for key in ["username", "password"]:
            if key in options:
                auth[key] = options[key]

        return auth


class LoggingMixin:
    def execute(self, *args, **options):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(options["verbosity"])
        )

        ch = logging.StreamHandler()
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        ch.setFormatter(formatter)

        logging.root.addHandler(ch)
        return super().execute(*args, **options)
