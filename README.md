# Тесты API Музея Метрополитен

Автоматизированные тесты для проверки API [Музея Метрополитен](https://metmuseum.github.io).
Написаны на Python с использованием Pytest и Pydantic.

## Что проверяется

- **`/objects/{objectID}`** — получение произведения по ID
  - корректный HTTP-статус (200)
  - валидация ответа Pydantic-моделью `MetObject`
  - обработка несуществующих ID (404)
  - Content-Type ответа
- **`/objects`** — список всех Object ID
  - соответствие схеме (`total`, `objectIDs`)
  - совпадение `total` и длины списка
  - уникальность и корректность ID
  - фильтры `departmentIds`, `metadataDate`
- **`/departments`** — список отделов музея
  - валидация схемы
  - уникальность `departmentId`
  - связка с поиском
- **`/v1.1/search`** — пагинированный поиск
  - поиск по ключевому слову
  - валидация структуры ответа
  - пагинация (`offset`, `limit`, ограничение 500)
  - фильтры (`isHighlight`, `departmentId`, `hasImages`, `dateBegin/End`, `medium`, `geoLocation`)
- **`/v1/search`** (устаревший) — проверка, что эндпоинт отключён (410 Gone)

## Стек

- Python 3.14
- pytest — движок тестов
- requests — HTTP-запросы
- pydantic — валидация данных

## Структура проекта
