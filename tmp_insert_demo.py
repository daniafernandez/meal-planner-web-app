from models.project_model import ProjectModel
from services.project_model import ProjectModelService


class ProjectService(ProjectModelService):
    collection_name = "projects"


def main() -> None:
    service = ProjectService()
    doc = ProjectModel(id="demo-project-1")
    inserted_id = service.insert_one_item(doc)
    print(f"Inserted id: {inserted_id}")


if __name__ == "__main__":
    main()
