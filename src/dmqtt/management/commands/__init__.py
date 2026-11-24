import logging

from django.conf import settings
from django.core.management.base import CommandParser

from dmqtt.shortcuts import default_client_id


class ClientMixin:
    def add_arguments(self, parser: CommandParser):
        mqtt = parser.add_argument_group("mqtt connection arguments")
        mqtt.add_argument("-u", "--username", default=settings.MQTT_USER)
        mqtt.add_argument("-P", "--password", default=settings.MQTT_PASS)
        mqtt.add_argument("-H", "--hostname", default=settings.MQTT_HOST)
        mqtt.add_argument("--port", default=settings.MQTT_PORT, type=int)
        mqtt.add_argument("--client-id", default=default_client_id())

    def client_arguments(self, options) -> dict:
        return {
            k: options[k]
            for k in [
                "qos",
                "retain",
                "client_id",
                "hostname",
                "port",
            ]
            if options.get(k)
        }

    def auth_arguments(self, options) -> dict:
        return {k: options[k] for k in ["username", "password"] if options.get(k)}


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
