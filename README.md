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
    print(topic)
    print(data)

@regex("^some/(?P<username>[^/]+)/(?P<device>[^/]+)$")
def regex_topic(match, data, **kwargs):
    device = match.groupdict()
    print(device['username'], device['device])
    print(data)
```

# Authentication

## mosquitto-go-auth

Used with <https://github.com/iegomez/mosquitto-go-auth>

```python
# From example project urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("mosquitto/", include("dmqtt.mosquitto")),
    path("account/", include(("django.contrib.auth.urls", "auth"), namespace="auth")),
    path("admin/", admin.site.urls),
]
```

```
# mosquitto configuration
# https://github.com/iegomez/mosquitto-go-auth#http
auth_plugin /mosquitto/go-auth.so
auth_opt_backends http
auth_opt_check_prefix false

auth_opt_http_host example.com
auth_opt_http_getuser_uri /mosquitto/getuser
auth_opt_http_aclcheck_uri /mosquitto/aclcheck

# If using https
auth_opt_http_port 443
auth_opt_http_with_tls true
```
