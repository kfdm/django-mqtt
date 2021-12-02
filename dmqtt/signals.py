import fnmatch
import json
import logging
import re

import django.dispatch

logger = logging.getLogger(__name__)

connect = django.dispatch.Signal(providing_args=["userdata", "flags", "rc"])
message = django.dispatch.Signal(providing_args=["userdata", "msg"])


def topic(matcher, as_json=True, **extras):
    def wrap(func):
        def inner(msg, **kwargs):
            if fnmatch.fnmatch(msg.topic, matcher):
                logger.debug("Matched %s for %s", matcher, func)
                if as_json:
                    kwargs["data"] = json.loads(msg.payload.decode("utf8"))
                func(topic=msg.topic, msg=msg, **kwargs)

        message.connect(inner, **extras)
        return inner

    return wrap


def regex(pattern, *, as_json=True, **extras):
    matcher = re.compile(pattern)

    def wrap(func):
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
