import logging

from models import DepartmentsResponse

logger = logging.getLogger(__name__)


class TestDepartments:
    """Тесты эндпоинта /departments."""

    def test_departments_status(self, api_client):
        """Успешный запрос возвращает 200."""
        response = api_client.get_departments()
        assert response.status_code == 200

    def test_departments_schema(self, api_client):
        """Ответ валидируется моделью DepartmentsResponse."""
        response = api_client.get_departments()
        data = DepartmentsResponse.model_validate(response.json())

        assert len(data.departments) > 0, "Список департаментов не должен быть пустым"
        logger.info("Получено департаментов: %d", len(data.departments))

    def test_department_ids_unique(self, api_client):
        """departmentId не должны повторяться."""
        data = DepartmentsResponse.model_validate(api_client.get_departments().json())
        ids = [d.departmentId for d in data.departments]

        assert len(ids) == len(set(ids)), "Найдены дублирующиеся departmentId"

    def test_department_names_not_empty(self, api_client):
        """У каждого департамента непустое displayName."""
        data = DepartmentsResponse.model_validate(api_client.get_departments().json())

        for d in data.departments:
            assert d.displayName.strip(), \
                f"Пустое имя у departmentId={d.departmentId}"

    def test_department_id_used_in_search(self, api_client):
        """departmentId из /departments действительно работает в /v1.1/search."""
        data = DepartmentsResponse.model_validate(api_client.get_departments().json())
        first_department_id = data.departments[0].departmentId

        response = api_client.search(q="cat", departmentId=first_department_id)
        assert response.status_code == 200