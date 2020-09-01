import logging

import paho.mqtt.client as mqtt

from dmqtt.signals import connect, message

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand

logging.basicConfig(level=logging.DEBUG)


class Client(mqtt.Client):
    def on_connect(self, client, userdata, flags, rc):
        connect.send(client, userdata=userdata, flags=flags, rc=rc)

    def on_message(self, client, userdata, msg):
        message.send(client, userdata=userdata, msg=msg)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-u", "--user", default=settings.MQTT_USER)
        parser.add_argument("-P", "--password", default=settings.MQTT_PASS)
        parser.add_argument("-H", "--host", default=settings.MQTT_HOST)
        parser.add_argument("--port", default=settings.MQTT_PORT, type=int)
        parser.add_argument("--client-id", default=get_current_site(None).domain)

    def handle(self, verbosity, **kwargs):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(verbosity)
        )

        client = Client(client_id=kwargs["client_id"])
        client.enable_logger()  # Use Python logging
        client.username_pw_set(kwargs["user"], password=kwargs["password"])
        # TODO Fix
        # client.tls_set()
        client.connect(kwargs["host"], kwargs["port"], 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            client.disconnect()
