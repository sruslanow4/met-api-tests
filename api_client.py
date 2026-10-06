import logging

import requests

logger = logging.getLogger(__name__)


class MetAPIClient:
    """Клиент для работы с API Музея Метрополитен."""

    BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"
    BASE_URL_V11 = "https://collectionapi.metmuseum.org/public/collection/v1.1"
    TIMEOUT = 30

    def __init__(self, session: requests.Session | None = None):
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, url: str, params: dict | None = None) -> requests.Response:
        """Внутренний метод: делает GET-запрос и логирует его."""
        logger.info("GET %s params=%s", url, params)

        response = self.session.get(url, params=params, timeout=self.TIMEOUT)

        logger.info("Response %s %s | size=%d bytes",
                    response.status_code, url, len(response.content))

        if response.status_code >= 400:
            logger.warning("Ошибка: тело ответа = %s", response.text[:300])
        else:
            logger.debug("Тело ответа: %s", response.text[:300])

        return response

    # ---- Endpoint: /objects ----
    def get_all_objects(self, **params) -> requests.Response:
        """GET /objects — список всех Object ID."""
        return self._request(f"{self.BASE_URL}/objects", params=params or None)

    # ---- Endpoint: /objects/{id} ----
    def get_object(self, object_id: int) -> requests.Response:
        """GET /objects/{objectID} — данные одного произведения."""
        return self._request(f"{self.BASE_URL}/objects/{object_id}")

    # ---- Endpoint: /departments ----
    def get_departments(self) -> requests.Response:
        """GET /departments — список отделов музея."""
        return self._request(f"{self.BASE_URL}/departments")

       # ---- Endpoint: /search (устаревший, отключён 2026-10-01) ----
    def search_v1(self, **params) -> requests.Response:
        """GET /search — устаревший поиск (возвращает 410)."""
        return self._request(f"{self.BASE_URL}/search", params=params or None)

    # ---- Endpoint: /v1.1/search (новый пагинированный поиск) ----
    def search(self, **params) -> requests.Response:
        """GET /v1.1/search — поиск Object ID с пагинацией."""
        return self._request(f"{self.BASE_URL_V11}/search", params=params or None)