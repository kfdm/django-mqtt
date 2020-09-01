import fnmatch
import json
import logging

import django.dispatch

logger = logging.getLogger(__name__)

connect = django.dispatch.Signal(providing_args=["userdata", "flags", "rc"])
message = django.dispatch.Signal(providing_args=["userdata", "msg"])


def topic(matcher, **extras):
    def wrap(func):
        def inner(msg, **kwargs):
            if fnmatch.fnmatch(msg.topic, matcher):
                logger.debug("Matched %s for %s", matcher, func)
                func(
                    topic=msg.topic,
                    data=json.loads(msg.payload.decode("utf8")),
                    **kwargs
                )

        message.connect(inner, **extras)
        return inner

    return wrap
