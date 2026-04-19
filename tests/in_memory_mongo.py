from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from pymongo.errors import DuplicateKeyError


@dataclass(frozen=True)
class MockMongoSettings:
    uri: str = "mongodb://mock"
    database: str = "meal_planner_test"


@dataclass(frozen=True)
class InMemoryInsertOneResult:
    inserted_id: int


@dataclass(frozen=True)
class InMemoryInsertManyResult:
    inserted_ids: list[int]


@dataclass(frozen=True)
class InMemoryUpdateResult:
    matched_count: int


class InMemoryMongoCollection:
    def __init__(self):
        self._documents: list[dict[str, Any]] = []
        self._unique_indexes: set[str] = set()

    def create_index(self, key: str, unique: bool = False) -> str:
        if unique:
            self._unique_indexes.add(key)
        return key

    def insert_one(self, doc: dict[str, Any]) -> InMemoryInsertOneResult:
        self._validate_unique_indexes(doc)
        self._documents.append(deepcopy(doc))
        return InMemoryInsertOneResult(inserted_id=len(self._documents))

    def insert_many(self, docs: list[dict[str, Any]]) -> InMemoryInsertManyResult:
        inserted_ids = [self.insert_one(doc).inserted_id for doc in docs]
        return InMemoryInsertManyResult(inserted_ids=inserted_ids)

    def find_one(self, filter: dict[str, Any]) -> dict[str, Any] | None:
        for document in self._documents:
            if self._matches_filter(document, filter):
                return deepcopy(document)
        return None

    def update_one(self, filter: dict[str, Any], update: dict[str, Any]) -> InMemoryUpdateResult:
        for document in self._documents:
            if self._matches_filter(document, filter):
                self._apply_update(document, update)
                return InMemoryUpdateResult(matched_count=1)
        return InMemoryUpdateResult(matched_count=0)

    def _validate_unique_indexes(self, doc: dict[str, Any]) -> None:
        for key in self._unique_indexes:
            if any(existing.get(key) == doc.get(key) for existing in self._documents):
                raise DuplicateKeyError(f"Duplicate key for '{key}'.")

    @staticmethod
    def _matches_filter(document: dict[str, Any], filter: dict[str, Any]) -> bool:
        return all(document.get(key) == value for key, value in filter.items())

    @staticmethod
    def _apply_update(document: dict[str, Any], update: dict[str, Any]) -> None:
        for field, value in update.get("$push", {}).items():
            document.setdefault(field, []).append(deepcopy(value))


class InMemoryMongoDatabase:
    def __init__(self):
        self._collections: dict[str, InMemoryMongoCollection] = {}

    def __getitem__(self, collection_name: str) -> InMemoryMongoCollection:
        if collection_name not in self._collections:
            self._collections[collection_name] = InMemoryMongoCollection()
        return self._collections[collection_name]


class InMemoryMongoClient:
    def __init__(self):
        self._databases: dict[str, InMemoryMongoDatabase] = {}

    def __getitem__(self, database_name: str) -> InMemoryMongoDatabase:
        if database_name not in self._databases:
            self._databases[database_name] = InMemoryMongoDatabase()
        return self._databases[database_name]
