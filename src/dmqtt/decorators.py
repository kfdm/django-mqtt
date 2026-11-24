import json
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")

# The JSONEncoder from DRF handles quite a few types, so we default to that
# if available and if not fallback to the Django one which still handles some
# extra types
try:
    from rest_framework.utils.encoders import JSONEncoder
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder


def json_payload(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator to add json support to MQTT publish methods
    """

    @wraps(func)
    def __inner(*args, **kwargs):
        if "json" in kwargs:
            data = kwargs.pop("json")
            kwargs["payload"] = json.dumps(data, cls=JSONEncoder).encode("utf8")

        return func(*args, **kwargs)

    return __inner
