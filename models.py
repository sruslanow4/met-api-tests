
from pydantic import BaseModel


class Constituent(BaseModel):
    """Один автор/участник создания произведения."""
    constituentID: int | None = None
    role: str | None = None
    name: str | None = None
    constituentULAN_URL: str | None = None
    constituentWikidata_URL: str | None = None
    gender: str | None = None


class Tag(BaseModel):
    """Тег (ключевое слово) произведения."""
    term: str | None = None
    AAT_URL: str | None = None
    Wikidata_URL: str | None = None


class MetObject(BaseModel):
    """Модель одного произведения искусства."""
    objectID: int
    isHighlight: bool | None = None
    accessionNumber: str | None = None
    accessionYear: str | None = None
    isPublicDomain: bool | None = None
    primaryImage: str | None = None
    primaryImageSmall: str | None = None
    additionalImages: list[str] | None = None
    constituents: list[Constituent] | None = None
    department: str | None = None
    objectName: str | None = None
    title: str | None = None
    artistDisplayName: str | None = None
    objectDate: str | None = None
    objectBeginDate: int | None = None
    objectEndDate: int | None = None
    medium: str | None = None
    creditLine: str | None = None
    classification: str | None = None
    linkResource: str | None = None
    metadataDate: str | None = None
    repository: str | None = None
    objectURL: str | None = None
    tags: list[Tag] | None = None


class ObjectListResponse(BaseModel):
    """Ответ /objects — список всех Object ID."""
    total: int
    objectIDs: list[int] | None = None
    
class SearchV11Response(BaseModel):
    """Ответ /v1.1/search — пагинированный поиск."""
    total: int
    objectIDs: list[int] | None = None
    
class Department(BaseModel):
    """Один отдел музея."""
    departmentId: int
    displayName: str


class DepartmentsResponse(BaseModel):
    """Ответ /departments — список отделов."""
    departments: list[Department]