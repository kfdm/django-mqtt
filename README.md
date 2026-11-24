# django-mqtt

MQTT tools for Django project

[![PyPI Version](https://img.shields.io/pypi/v/django-mqtt)](https://pypi.org/project/django-mqtt)
[![PyPI Status](https://img.shields.io/pypi/status/django-mqtt)](https://pypi.org/project/django-mqtt)
[![PyPI License](https://img.shields.io/pypi/l/django-mqtt)](https://pypi.org/project/django-mqtt)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-mqtt/)

# Installation

```python
# In your settings.py
# Update INSTALLED APPS
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "...",
    "dmqtt", # << Add this to your apps
]

# Configure connection settings
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_PASS = "testing"
MQTT_USER = "testing"

# Optional TLS settings
# https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html#paho.mqtt.client.Client.tls_set
MQTT_TLS = {}
```

# Usage

```shell
# Launch client that will listen to mqtt messages
python manage.py mqtt

# or send a test message to your broker
echo 'test-message' | python.manage mqtt my-topic
```

Configure senders to listen to mqtt signals

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
    print(device["username"], device["device"])
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
