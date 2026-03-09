from django.utils.module_loading import import_string
from django.conf import settings
import logging

import paho.mqtt.client as mqtt


from dmqtt.shortcuts import json_payload
from dmqtt.signals import connect, message


class Client(mqtt.Client):
    def on_connect(self, client, userdata, flags, rc):
        connect.send_robust(client, userdata=userdata, flags=flags, rc=rc)

    def on_message(self, client, userdata, msg):
        if logging.root.isEnabledFor(logging.INFO):
            try:
                if msg.retain:
                    print("*", end=" ")
                print(msg.topic, msg.payload.decode("utf8"))
            except UnicodeDecodeError:
                print(msg.topic, "** Unknown Encoding **")
        message.send_robust(client, userdata=userdata, msg=msg)

    publish = json_payload(mqtt.Client.publish)


def get_client() -> type[Client]:
    class_path = getattr(settings, "MQTT_CLIENT", "dmqtt.client.Client")
    return import_string(class_path)
