# 0.4.2 - 2023-02-18

- [BUGFIX] Only use get_current_site if django.contrib.sites is installed.
- [IMPROVEMENT]Allow overriding client_id to shortcuts.single
- [IMPROVEMENT] Allow overriding mysql_client Class
- [INTERNAL] Migrate to pyproject.toml

# 0.4.0 - 2022-07-04

- [IMPROVEMENT] Remove djangorestframework requirement #3
- [INTERNAL] Add initial set of unittests

# 0.3.0 - 2022-06-16

- [IMPROVEMENT] Use rest_framework JSONEncoder if available, fall back to Django
- [IMPROVEMENT] Only apply auth if MQTT_USER and MQTT_PASS are set
