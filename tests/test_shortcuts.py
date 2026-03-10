from unittest import mock

from . import BaseTest
from dmqtt import shortcuts


class ShortcutTests(BaseTest):
    @mock.patch("paho.mqtt.publish.multiple")
    def test_single(self, mock_multiple: mock.MagicMock):
        shortcuts.single(topic="test", json={"foo": "bar"})
        mock_multiple.assert_called_with(
            [{"topic": "test", "payload": b'{"foo": "bar"}', "qos": 0, "retain": False}],
            hostname="localhost",
            port=1883,
            # Can't easily test the specific value because it's random
            client_id=mock.ANY,
            auth={"username": "testing", "password": "testing"},
        )
