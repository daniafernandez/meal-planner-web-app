from typing import Any, Protocol

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from models.project_model import ProjectModel
from settings import MongoSettings
from services.errors import DuplicateResourceError


class MongoSettingsProtocol(Protocol):
    uri: str
    database: str


class InsertOneResultProtocol(Protocol):
    inserted_id: Any


class InsertManyResultProtocol(Protocol):
    inserted_ids: list[Any]


class UpdateResultProtocol(Protocol):
    matched_count: int


class CollectionProtocol(Protocol):
    def create_index(self, key: str, unique: bool = False) -> Any: ...

    def insert_one(self, doc: dict[str, Any]) -> InsertOneResultProtocol: ...

    def insert_many(self, docs: list[dict[str, Any]]) -> InsertManyResultProtocol: ...

    def find_one(self, filter: dict[str, Any]) -> dict[str, Any] | None: ...

    def update_one(self, filter: dict[str, Any], update: dict[str, Any]) -> UpdateResultProtocol: ...


class DatabaseProtocol(Protocol):
    def __getitem__(self, collection_name: str) -> CollectionProtocol: ...


class MongoClientProtocol(Protocol):
    def __getitem__(self, database_name: str) -> DatabaseProtocol: ...


class ProjectModelService:
    collection_name: str | None = None

    def __init__(
        self,
        settings: MongoSettingsProtocol | None = None,
        client: MongoClientProtocol | None = None,
        collection: CollectionProtocol | None = None,
    ):
        if collection is not None:
            self.collection = collection
            return

        if not self.collection_name:
            raise ValueError("collection_name must be set on the service class.")

        resolved_settings = settings or MongoSettings()
        resolved_client = client or MongoClient(resolved_settings.uri)
        self.collection = resolved_client[resolved_settings.database][self.collection_name]

    def insert_one_item(self, data: ProjectModel) -> int:
        doc = data.model_dump()
        try:
            result = self.collection.insert_one(doc)
        except DuplicateKeyError as exc:
            raise DuplicateResourceError(f"Duplicate id '{data.id}'.") from exc
        return result.inserted_id

    def validate_unique_field(self, field_name: str, field_value: Any) -> None:
        if self.collection.find_one({field_name: field_value}) is not None:
            raise DuplicateResourceError(f"Duplicate {field_name} '{field_value}'.")

    def insert_many_items(self, data: list[ProjectModel]) -> list[int]:
        docs = [item.model_dump() for item in data]
        result = self.collection.insert_many(docs)
        return result.inserted_ids

    def get_one_item_by_id(self, id: str) -> ProjectModel:
        item = self.collection.find_one({"id": id})
        return ProjectModel(**item)
