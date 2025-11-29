from dmqtt.signals import convert_wildcards


from . import BaseTest


class WildcardTest(BaseTest):
    def test_single_level_wildcard(self):
        pattern = convert_wildcards("home/+/status")
        assert pattern.match("home/kitchen/status")
        assert not pattern.match("home/kitchen/lights/status")

    def test_multi_level_wildcard(self):
        pattern = convert_wildcards("home/#")
        assert pattern.match("home/kitchen/status")
        assert pattern.match("home/kitchen/lights/status")

    def test_mixed_wildcards(self):
        pattern = convert_wildcards("home/+/lights/#")
        assert pattern.match("home/kitchen/lights/status")
        assert pattern.match("home/bathroom/lights/brightness/set")
        assert not pattern.match("home/status")
