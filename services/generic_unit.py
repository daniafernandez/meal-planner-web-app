from models.generic_unit import GenericUnit, get_equivalent_generic_unit_names
from services import ProjectModelService
from services.errors import DuplicateResourceError


class GenericUnitService(ProjectModelService):
    collection_name = "generic_units"

    def create_generic_unit(self, generic_unit: GenericUnit) -> GenericUnit:
        self.validate_unique_field("name", generic_unit.name)
        self.validate_unique_equivalent_name(generic_unit)
        self.insert_one_item(generic_unit)
        return generic_unit

    def validate_unique_equivalent_name(self, generic_unit: GenericUnit) -> None:
        equivalent_names = get_equivalent_generic_unit_names(generic_unit.name) - {generic_unit.name}
        for equivalent_name in equivalent_names:
            existing_generic_unit = self.collection.find_one({"name": equivalent_name})
            if existing_generic_unit is not None:
                raise DuplicateResourceError(
                    f'Equivalent generic unit with name: "{existing_generic_unit["name"]}" already exists.',
                )

    def get_generic_unit_by_id(self, generic_unit_id: str) -> GenericUnit | None:
        item = self.collection.find_one({"id": generic_unit_id})
        if item is None:
            return None
        return GenericUnit(**item)
