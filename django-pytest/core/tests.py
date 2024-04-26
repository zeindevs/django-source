import logging
from django.test import TestCase, Client, override_settings


# Create your tests here.
class MaintenanceModeMiddlewareTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        logging.disable(logging.CRITICAL)

    @override_settings(MAINTENANCE_MODE=True)
    def test_response_when_maintenance_mode_is_on(self) -> None:
        response = self.client.get("/")
        self.assertContains(
            response, "Oops! We are currently working on some updates."
        )

    @override_settings(MAINTENANCE_MODE=False)
    def test_response_when_maintenance_mode_is_off(self) -> None:
        response = self.client.get("/")
        self.assertContains(response, "We're in!")
        self.assertTemplateUsed(response, "index.html")
