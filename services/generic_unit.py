from models.generic_unit import GenericUnit
from services import ProjectModelService


class GenericUnitService(ProjectModelService):
    collection_name = "generic_units"

    def create_generic_unit(self, generic_unit: GenericUnit) -> GenericUnit:
        self.validate_unique_field("name", generic_unit.name)
        self.insert_one_item(generic_unit)
        return generic_unit

    def get_generic_unit_by_id(self, generic_unit_id: str) -> GenericUnit | None:
        item = self.collection.find_one({"id": generic_unit_id})
        if item is None:
            return None
        return GenericUnit(**item)
