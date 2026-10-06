import logging

import pytest

from models import MetObject

logger = logging.getLogger(__name__)


class TestGetObject:
    """Тесты эндпоинта /objects/{objectID}."""

    def test_get_existing_object(self, api_client):
        """Существующий объект: статус 200 и валидация Pydantic-модели."""
        object_id = 436535  # Ван Гог, «Пшеничное поле с кипарисами»

        response = api_client.get_object(object_id)

        assert response.status_code == 200, \
            f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        obj = MetObject.model_validate(data)

        assert obj.objectID == object_id
        logger.info("Объект %s: title=%r, artist=%r",
                    obj.objectID, obj.title, obj.artistDisplayName)

    def test_object_has_title(self, api_client):
        """У реального объекта должно быть непустое название."""
        response = api_client.get_object(436535)
        obj = MetObject.model_validate(response.json())

        assert obj.title, "Название произведения не должно быть пустым"

    def test_object_has_artist(self, api_client):
        """У картины Ван Гога должен быть указан автор."""
        response = api_client.get_object(436535)
        obj = MetObject.model_validate(response.json())

        assert obj.artistDisplayName == "Vincent van Gogh"

    @pytest.mark.parametrize("invalid_id", [999999999, 0, -1])
    def test_nonexistent_object_returns_404(self, api_client, invalid_id):
        """Несуществующий или некорректный ID → 404."""
        response = api_client.get_object(invalid_id)

        assert response.status_code == 404, \
            f"Для ID={invalid_id} ожидался 404, получен {response.status_code}"

    def test_object_content_type_json(self, api_client):
        """Content-Type ответа — application/json."""
        response = api_client.get_object(436535)

        assert "application/json" in response.headers.get("Content-Type", "")