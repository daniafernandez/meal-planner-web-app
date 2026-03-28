from pymongo import MongoClient
from pymongo.collection import Collection

from models.project_model import ProjectModel
from settings import MongoSettings


class ProjectModelService:
    collection_name: str | None = None

    def __init__(
        self,
        settings: MongoSettings | None = None,
        client: MongoClient | None = None,
        collection: Collection | None = None,
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
        result = self.collection.insert_one(doc)
        return result.inserted_id

    def insert_many_items(self, data: list[ProjectModel]) -> list[int]:
        docs = [item.model_dump() for item in data]
        result = self.collection.insert_many(docs)
        return result.inserted_ids

    def get_one_item_by_id(self, id: str) -> ProjectModel:
        item = self.collection.find_one({'_id': id})
        return ProjectModel(**item)
