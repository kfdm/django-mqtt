import json
import logging
import os

import paho.mqtt.client as mqtt

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand

from dmqtt.signals import connect, message

logging.basicConfig(level=logging.DEBUG)


class Client(mqtt.Client):
    def on_connect(self, client, userdata, flags, rc):
        connect.send_robust(client, userdata=userdata, flags=flags, rc=rc)

    def on_message(self, client, userdata, msg):
        if logging.root.isEnabledFor(logging.INFO):
            try:
                print(msg.topic, msg.payload.decode("utf8"))
            except UnicodeDecodeError:
                print(msg.topic, "** Unknown Encoding **")
        message.send_robust(client, userdata=userdata, msg=msg)

    def publish(self, topic, **kwargs):
        if "json" in kwargs:
            data = kwargs.pop("json")
            kwargs["payload"] = json.dumps(data)
        super().publish(topic, **kwargs)


class Command(BaseCommand):
    def add_arguments(self, parser):
        domain = get_current_site(None).domain
        pid = os.getpid()
        parser.add_argument("-u", "--user", default=settings.MQTT_USER)
        parser.add_argument("-P", "--password", default=settings.MQTT_PASS)
        parser.add_argument("-H", "--host", default=settings.MQTT_HOST)
        parser.add_argument("--port", default=settings.MQTT_PORT, type=int)
        parser.add_argument("--client-id", default=f"{domain}-{pid}")

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
