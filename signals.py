import fnmatch
import json
import django.dispatch

import logging

logger = logging.getLogger(__name__)

connect = django.dispatch.Signal(providing_args=["userdata", "flags", "rc"])
message = django.dispatch.Signal(providing_args=["userdata", "msg"])


def glob(matcher):
    def wrap(func):
        def inner(msg, **kwargs):
            if fnmatch.fnmatch(msg.topic, matcher):
                logger.debug("Matched %s for %s", matcher, func)
                func(
                    topic=msg.topic,
                    data=json.loads(msg.payload.decode("utf8")),
                    **kwargs
                )

        return inner

    return wrap
