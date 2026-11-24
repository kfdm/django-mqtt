from django.apps import AppConfig


class MqttConfig(AppConfig):
    name = "tests.example"

    def ready(self):
        pass
