from django.apps import AppConfig


class Config(AppConfig):
    name = __package__

    def ready(self):
        import dmqtt.checks  # NOQA: F401
