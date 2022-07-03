from unittest import mock

from . import BaseTest


class LoginTest(BaseTest):
    fixtures = ["default"]

    @mock.patch("django.contrib.auth.signals.user_login_failed.send")
    @mock.patch("django.contrib.auth.signals.user_logged_in.send")
    def test_successfull_login(self, signal_success, signal_failed):
        result = self.client.post(
            "/mosquitto/getuser",
            data={"username": "sample-user", "password": "sample-password"},
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 200, result.content.decode("utf8"))
        self.assertEqual(signal_success.call_count, 1, "Called user_logged_in signal")
        self.assertEqual(signal_failed.call_count, 0, "Skipped user_login_failed signal")

    @mock.patch("django.contrib.auth.signals.user_login_failed.send")
    @mock.patch("django.contrib.auth.signals.user_logged_in.send")
    def test_failed_login(self, signal_success, signal_failed):
        result = self.client.post(
            "/mosquitto/getuser",
            data={"username": "sample-user", "password": "invalid-password"},
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 403, result.content.decode("utf8"))
        self.assertEqual(signal_success.call_count, 0, "Skipped user_logged_in signal")
        self.assertEqual(signal_failed.call_count, 1, "Called user_login_failed signal")

    @mock.patch("django.contrib.auth.signals.user_login_failed.send")
    @mock.patch("django.contrib.auth.signals.user_logged_in.send")
    def test_missing_user(self, signal_success, signal_failed):
        result = self.client.post(
            "/mosquitto/getuser",
            data={"username": "missing-user", "password": "invalid-password"},
            content_type="application/json",
        )

        self.assertEqual(result.status_code, 403, result.content.decode("utf8"))
        self.assertEqual(signal_success.call_count, 0, "Skipped user_logged_in signal")
        self.assertEqual(signal_failed.call_count, 1, "Called user_login_failed signal")
