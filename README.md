# django-mqtt

MQTT tools for Django project

[![PyPI](https://img.shields.io/pypi/v/django-mqtt)](https://pypi.org/project/django-mqtt/)

# Usage

- Add `"dmqtt"` to your `INSTALLED_APPS`
- Add `MQTT_HOST`, `MQTT_USER`, `MQTT_PASS`, `MQTT_PORT`
- Run with `python manage.py mqtt`

```python
from dmqtt.signals import connect, regex, topic
from django.dispatch import receiver

@receiver(connect)
def on_connect(sender, **kwargs):
    sender.subscribe("#")

@topic("some/mqtt/topic")
def simple_topic(sender, topic, data, **kwargs):
    pass

@regex("^some/(?P<username>[^/]+)/(?P<topic>[^/]+)$")
def regex_topic(match, data, **kwargs):
    device = match.groupdict()
```
