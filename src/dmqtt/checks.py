from django.core.checks import Error, register
from django.conf import settings


setting_names = [
    "MQTT_HOST",
    "MQTT_USER",
    "MQTT_PASS",
    "MQTT_PORT",
]


@register()
def settings_check(app_configs, **kwargs):
    for name in setting_names:
        if not hasattr(settings, name):
            yield Error(
                msg=f"Missing setting {name}",
                hint=f"Need to add {name} to {settings.SETTINGS_MODULE}",
                obj=settings,
            )
