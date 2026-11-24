from django.test import TestCase
from django.test.client import Client


class BaseTest(TestCase):
    fixtures = ["default"]  # NOQA: RUF012

    def setUp(self):
        super().setUp()
        self.client = Client(enforce_csrf_checks=True)
