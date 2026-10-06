import logging
import sys

import pytest
import requests

from api_client import MetAPIClient


def pytest_configure(config):
    """Настройка логирования при запуске pytest."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("met_api_tests.log", mode="w", encoding="utf-8"),
        ],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)


@pytest.fixture(scope="session")
def api_client():
    """Один общий клиент API на все тесты."""
    session = requests.Session()
    session.headers.update({"User-Agent": "MetAPITests/1.0"})
    yield MetAPIClient(session=session)
    session.close()