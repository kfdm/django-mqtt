from django.core.management.base import BaseCommand, CommandParser
from django.test import override_settings

from dmqtt.client import Client, get_client

from . import ClientMixin, LoggingMixin


class Command(ClientMixin, LoggingMixin, BaseCommand):
    def get_mqtt_client(self) -> type[Client]:
        return get_client()

    def add_arguments(self, parser: CommandParser):
        super().add_arguments(parser)
        celery = parser.add_argument_group("celery arguments")
        celery.add_argument("--eager", action="store_true")

    def handle(self, eager, **options):
        client = self.get_mqtt_client()(client_id=options["client_id"])
        client.enable_logger()  # Use Python logging

        if auth := self.auth_arguments(options):
            client.username_pw_set(**auth)

        if tls := self.tls_arguments(options):
            client.tls_set(**tls)

        client.connect(options["hostname"], options["port"], 60)

        try:
            from setproctitle import setproctitle
        except ImportError:
            pass
        else:
            if client._client_id:
                setproctitle(f"[mqtt] {client._client_id.decode('utf8')}")

        with override_settings(CELERY_TASK_ALWAYS_EAGER=eager):
            # Blocking call that processes network traffic, dispatches callbacks and
            # handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a
            # manual interface.
            try:
                client.loop_forever()
            except KeyboardInterrupt:
                client.disconnect()
