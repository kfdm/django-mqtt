import fnmatch
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


def topic(matcher, as_json=True, **extras):
    def wrap(func):
        @functools.wraps(func)
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
