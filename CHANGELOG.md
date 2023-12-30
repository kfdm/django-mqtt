# 0.4.0 - 2023-12-30

- [BUGFIX] Only use get_current_site if django.contrib.sites installed.

# 0.4.0 - 2022-07-04

- [IMPROVEMENT] Remove djangorestframework requirement #3
- [INTERNAL] Add initial set of unittests

# 0.3.0 - 2022-06-16

- [IMPROVEMENT] Use rest_framework JSONEncoder if available, fall back to Django
- [IMPROVEMENT] Only apply auth if MQTT_USER and MQTT_PASS are set
