from django.core.checks import Error, register, Warning
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


@register()
def signals_check(app_configs, **kwargs):
    from . import signals

    check_signals = {
        "dmqtt.signals.connect": signals.connect,
        "dmqtt.signals.message": signals.message,
    }

    for name in check_signals:
        if not check_signals[name].has_listeners():
            yield Warning(
                msg=f"Missing recivers for {name}",
                hint="Ensure that your signals are loaded in your AppConfig.ready method",
            )
