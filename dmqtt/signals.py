import fnmatch
import functools
import json
import logging
import re

import django.dispatch

logger = logging.getLogger(__name__)

try:
    connect = django.dispatch.Signal(providing_args=["userdata", "flags", "rc"])
    message = django.dispatch.Signal(providing_args=["userdata", "msg"])
except TypeError:
    # for Django < 3.0
    connect = django.dispatch.Signal()
    message = django.dispatch.Signal()

def convert_wildcards(mqtt_topic):
    """Convert MQTT wildcards to regex pattern.
    '#' becomes '.*' (multi-level)
    '+' becomes '[^/]+' (single-level)
    """
    pattern = re.escape(mqtt_topic)
    pattern = pattern.replace('\\#', '.*')
    pattern = pattern.replace('\\+', '[^/]+')
    return '^' + pattern + '$'

def topic(matcher, as_json=True, **extras):
    def wrap(func):
        @functools.wraps(func)
        def inner(msg, **kwargs):
            nonlocal matcher
            regex_pattern = convert_wildcards(matcher)
            if re.match(regex_pattern, msg.topic):
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
