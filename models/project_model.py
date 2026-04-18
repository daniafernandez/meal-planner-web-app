from pydantic import BaseModel, ConfigDict


class ProjectModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
