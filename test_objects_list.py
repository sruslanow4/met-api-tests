import logging

from models import ObjectListResponse

logger = logging.getLogger(__name__)


class TestObjectsList:
    """Тесты эндпоинта /objects — список всех Object ID."""

    def test_objects_status(self, api_client):
        """Успешный запрос возвращает 200."""
        response = api_client.get_all_objects()
        assert response.status_code == 200

    def test_objects_schema(self, api_client):
        """Ответ валидируется моделью ObjectListResponse."""
        response = api_client.get_all_objects()
        data = ObjectListResponse.model_validate(response.json())

        assert data.total > 0, "Всего объектов должно быть больше нуля"
        assert data.objectIDs, "Список objectIDs не должен быть пустым"

        logger.info("Всего объектов: %d, получено ID: %d",
                    data.total, len(data.objectIDs))

    def test_objects_count_matches_total(self, api_client):
        """len(objectIDs) == total для запроса без фильтров."""
        data = ObjectListResponse.model_validate(api_client.get_all_objects().json())

        assert len(data.objectIDs) == data.total, \
            f"total={data.total}, но получено {len(data.objectIDs)}"

    def test_objects_ids_are_positive_ints(self, api_client):
        """Все ID — положительные целые числа."""
        data = ObjectListResponse.model_validate(api_client.get_all_objects().json())

        for oid in data.objectIDs[:100]:  # проверим первые 100
            assert isinstance(oid, int) and oid > 0, \
                f"Некорректный ID: {oid!r}"

    def test_objects_ids_unique(self, api_client):
        """ID в списке не должны повторяться (первые 1000)."""
        data = ObjectListResponse.model_validate(api_client.get_all_objects().json())
        sample = data.objectIDs[:1000]

        assert len(sample) == len(set(sample)), \
            "Найдены дублирующиеся objectID"

    def test_objects_filter_by_department(self, api_client):
        """Фильтр по departmentIds возвращает валидный ответ."""
        response = api_client.get_all_objects(departmentIds=1)
        assert response.status_code == 200

        data = ObjectListResponse.model_validate(response.json())
        assert data.total >= 0

    def test_objects_filter_multiple_departments(self, api_client):
        """Несколько departmentIds через | работают."""
        response = api_client.get_all_objects(departmentIds="3|9|12")
        assert response.status_code == 200
        ObjectListResponse.model_validate(response.json())

    def test_objects_metadata_date_filter(self, api_client):
        """Фильтр metadataDate возвращает валидный ответ."""
        response = api_client.get_all_objects(metadataDate="2018-10-22")
        assert response.status_code == 200
        ObjectListResponse.model_validate(response.json())