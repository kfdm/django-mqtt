# 0.7.0 - 2026-05-30

- [INTERNAL]: Add pre-commit config
- [IMPROVEMENT]: Add check for signals

# 0.6.0 - 2026-03-10

- [IMPROVEMENT] Add `dmqtt.shortcuts.multiple` to match our earlier `single` shortcut and be more compatible with upstream.
- [IMPROVEMENT] Add support for django checks framework
- [IMPROVEMENT] Use dmqtt.client.get_client() and `MQTT_CLIENT` setting to replace with custom client
- [INTERNAL] Cleanup of decorators and add more type hints
- [INTERNAL] Move our mqtt.Client to dmqtt.client to be easier to extend and use with type hinting

# 0.5.0 - 2025-11-29

- [INTERNAL] Switch to uv_build and move to src layout
- [BUGFIX] Fix handling of wildcards by compiling as regex

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
