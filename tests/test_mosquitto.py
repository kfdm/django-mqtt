from unittest import mock

from django.test import TestCase


class LoginTest(TestCase):
    fixtures = ["default"]

    @mock.patch("django.contrib.auth.signals.user_login_failed.send")
    @mock.patch("django.contrib.auth.signals.user_logged_in.send")
    def test_successfull_login(self, signal_success, signal_failed):
        result = self.client.post(
            "/mosquitto/getuser",
            data={"username": "sample-user", "password": "sample-password"},
            content_type="application/json",
        )

        self.assertEqual(signal_success.call_count, 1, "Called user_logged_in signal")
        self.assertEqual(signal_failed.call_count, 0, "Skipped user_login_failed signal")
        self.assertEqual(result.status_code, 200, "Returned 200")

    @mock.patch("django.contrib.auth.signals.user_login_failed.send")
    @mock.patch("django.contrib.auth.signals.user_logged_in.send")
    def test_failed_login(self, signal_success, signal_failed):
        result = self.client.post(
            "/mosquitto/getuser",
            data={"username": "sample-user", "password": "invalid-password"},
            content_type="application/json",
        )

        self.assertEqual(signal_success.call_count, 0, "Skipped user_logged_in signal")
        self.assertEqual(signal_failed.call_count, 1, "Called user_login_failed signal")
        self.assertEqual(result.status_code, 403, "Returned 403")

    @mock.patch("django.contrib.auth.signals.user_login_failed.send")
    @mock.patch("django.contrib.auth.signals.user_logged_in.send")
    def test_missing_user(self, signal_success, signal_failed):
        result = self.client.post(
            "/mosquitto/getuser",
            data={"username": "missing-user", "password": "invalid-password"},
            content_type="application/json",
        )

        self.assertEqual(signal_success.call_count, 0, "Skipped user_logged_in signal")
        self.assertEqual(signal_failed.call_count, 1, "Called user_login_failed signal")
        self.assertEqual(result.status_code, 403, "Returned 403")
