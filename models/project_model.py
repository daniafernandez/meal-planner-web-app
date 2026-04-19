from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ProjectModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(default_factory=lambda: str(uuid4()))
