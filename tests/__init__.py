from django.test import TestCase
from django.test.client import Client


class BaseTest(TestCase):
    fixtures = ["default"]

    def setUp(self):
        super().setUp()
        self.client = Client(enforce_csrf_checks=True)
