import fnmatch
import re
from dmqtt.signals import convert_wildcards


def test_single_level_wildcard():
    pattern = convert_wildcards("home/+/status")
    assert re.match(pattern, "home/kitchen/status")
    assert not re.match(pattern, "home/kitchen/lights/status")

def test_multi_level_wildcard():
    pattern = convert_wildcards("home/#")
    assert re.match(pattern, "home/kitchen/status")
    assert re.match(pattern, "home/kitchen/lights/status")

def test_mixed_wildcards():
    pattern = convert_wildcards("home/+/lights/#")
    assert re.match(pattern, "home/kitchen/lights/status")
    assert re.match(pattern, "home/bathroom/lights/brightness/set")
    assert not re.match(pattern, "home/status")