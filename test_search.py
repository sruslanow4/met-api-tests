import logging

from models import MetObject, SearchV11Response

logger = logging.getLogger(__name__)


class TestSearch:
    """Тесты эндпоинта /v1.1/search."""

    def test_search_by_keyword(self, api_client):
        """Поиск 'sunflowers' находит результаты и валидируется моделью."""
        response = api_client.search(q="sunflowers")

        assert response.status_code == 200, \
            f"Ожидался 200, получен {response.status_code}"

        data = SearchV11Response.model_validate(response.json())

        assert data.total > 0, "По запросу 'sunflowers' ничего не найдено"
        assert data.objectIDs, "Список objectIDs не должен быть пустым"

        logger.info("Поиск 'sunflowers': total=%d, на странице=%d",
                    data.total, len(data.objectIDs))

    def test_search_result_is_valid_object(self, api_client):
        """Первый найденный ID разворачивается в валидный MetObject."""
        search = SearchV11Response.model_validate(
            api_client.search(q="sunflowers").json()
        )
        first_id = search.objectIDs[0]

        response = api_client.get_object(first_id)
        assert response.status_code == 200

        obj = MetObject.model_validate(response.json())
        assert obj.objectID == first_id

    def test_search_no_results(self, api_client):
        """Бессмысленный запрос → total=0 и пустой список."""
        response = api_client.search(q="zzzqqqxxx_nonexistent_term_12345")

        assert response.status_code == 200
        data = SearchV11Response.model_validate(response.json())

        assert data.total == 0
        assert not data.objectIDs

    def test_search_default_page_size(self, api_client):
        """Без limit возвращается не больше 100 ID (значение по умолчанию)."""
        response = api_client.search(q="sunflowers")
        data = SearchV11Response.model_validate(response.json())

        assert len(data.objectIDs) <= 100, \
            f"По умолчанию должно быть ≤100, получено {len(data.objectIDs)}"

    def test_search_with_limit(self, api_client):
        """Явный limit ограничивает размер страницы."""
        response = api_client.search(q="sunflowers", limit=5)
        assert response.status_code == 200

        data = SearchV11Response.model_validate(response.json())
        assert len(data.objectIDs) <= 5

    def test_search_limit_capped_at_500(self, api_client):
        """limit=1000 должен обрезаться до 500."""
        response = api_client.search(q="cat", limit=1000)
        assert response.status_code == 200

        data = SearchV11Response.model_validate(response.json())
        assert len(data.objectIDs) <= 500, \
            f"limit должен быть ограничен 500, получено {len(data.objectIDs)}"

    def test_search_offset_changes_results(self, api_client):
        """Разные offset дают разные страницы."""
        page1 = SearchV11Response.model_validate(
            api_client.search(q="sunflowers", offset=0, limit=5).json()
        )
        page2 = SearchV11Response.model_validate(
            api_client.search(q="sunflowers", offset=5, limit=5).json()
        )

        assert page1.objectIDs != page2.objectIDs, \
            "Страницы с разным offset не должны совпадать"

    def test_search_total_same_across_pages(self, api_client):
        """total не зависит от страницы — это полное число совпадений."""
        r1 = SearchV11Response.model_validate(
            api_client.search(q="sunflowers", offset=0, limit=5).json()
        )
        r2 = SearchV11Response.model_validate(
            api_client.search(q="sunflowers", offset=10, limit=5).json()
        )

        assert r1.total == r2.total

    def test_search_is_highlight_filter(self, api_client):
        """Фильтр isHighlight=true."""
        response = api_client.search(q="sunflowers", isHighlight="true")
        assert response.status_code == 200
        SearchV11Response.model_validate(response.json())

    def test_search_department_filter(self, api_client):
        """Фильтр departmentId."""
        response = api_client.search(q="cat", departmentId=6)
        assert response.status_code == 200
        SearchV11Response.model_validate(response.json())

    def test_search_has_images_filter(self, api_client):
        """Фильтр hasImages=true."""
        response = api_client.search(q="renoir", hasImages="true")
        assert response.status_code == 200
        SearchV11Response.model_validate(response.json())

    def test_search_date_range_filter(self, api_client):
        """Фильтр по диапазону дат."""
        response = api_client.search(
            q="african", dateBegin=1700, dateEnd=1800
        )
        assert response.status_code == 200
        SearchV11Response.model_validate(response.json())

    def test_search_without_q_works_on_v11(self, api_client):
        """
        /v1.1 не требует q — фильтры без поискового слова работают
        (на старом /v1 это была ошибка).
        """
        response = api_client.search(hasImages="true", departmentId=11)
        assert response.status_code == 200
        SearchV11Response.model_validate(response.json())


class TestSearchV1Deprecated:
    """Тесты устаревшего /v1/search — проверяем, что он отключён."""

    def test_old_search_returns_410(self, api_client):
        """Старый /v1/search должен вернуть 410 Gone (отключён 2026-10-01)."""
        response = api_client.search_v1(q="sunflowers")
        assert response.status_code == 410, \
            f"Ожидался 410 (отключён), получен {response.status_code}"