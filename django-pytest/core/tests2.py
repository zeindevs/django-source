import logging
import pytest
from pytest_django.asserts import assertTemplateNotUsed, assertTemplateUsed


@pytest.fixture(autouse=True)
def disale_logging():
    logging.disable(logging.CRITICAL)


@pytest.fixture
def maintenance_mode_on(settings):
    settings.MAINTENANCE_MODE = True


@pytest.fixture
def maintenance_mode_off(settings):
    settings.MAINTENANCE_MODE = False


def test_response_when_maintenance_mode_is_on(maintenance_mode_on, client):
    response = client.get("/")
    response_text = "Oops! We are currently working on some updates."
    assert response_text in response.content.decode()


def test_response_when_maintenance_mode_is_off(maintenance_mode_off, client):
    response = client.get("/")
    response_text = "We're in!"
    assert response_text in response.content.decode()
    assertTemplateNotUsed("index.html")
