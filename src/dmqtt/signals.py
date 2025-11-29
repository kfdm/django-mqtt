import functools
import json
import logging
import re

import django.dispatch

logger = logging.getLogger(__name__)

# userdata, flags, rc
connect = django.dispatch.Signal()
# userdata, msg
message = django.dispatch.Signal()


def convert_wildcards(mqtt_topic) -> re.Pattern:
    """Convert MQTT wildcards to regex pattern.
    '#' becomes '.*' (multi-level)
    '+' becomes '[^/]+' (single-level)
    """
    pattern = re.escape(mqtt_topic)
    pattern = pattern.replace("\\#", ".*")
    pattern = pattern.replace("\\+", "[^/]+")
    return re.compile("^" + pattern + "$")


def topic(matcher, as_json=True, **extras):
    regex_pattern = convert_wildcards(matcher)

    def wrap(func):
        @functools.wraps(func)
        def inner(msg, **kwargs):
            if regex_pattern.match(msg.topic):
                logger.debug("Matched %s for %s", regex_pattern, func)
                if as_json:
                    kwargs["data"] = json.loads(msg.payload.decode("utf8"))
                func(topic=msg.topic, msg=msg, **kwargs)

        message.connect(inner, **extras)
        return inner

    return wrap


def regex(pattern, *, as_json=True, **extras):
    matcher = re.compile(pattern)

    def wrap(func):
        @functools.wraps(func)
        def inner(msg, **kwargs):
            match = matcher.match(msg.topic)
            if match:
                logger.debug("Matched %s for %s", match, func)
                if as_json:
                    kwargs["data"] = json.loads(msg.payload.decode("utf8"))
                func(topic=msg.topic, match=match, msg=msg, **kwargs)

        message.connect(inner, **extras)
        return inner

    return wrap
