from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.resources.endpoints import router
from services.generic_unit import GenericUnitService
from services.ingredient import IngredientService


ingredient_service = IngredientService()
generic_unit_service = GenericUnitService()


@asynccontextmanager
async def lifespan(_: FastAPI):
    ingredient_service.collection.create_index("id", unique=True)
    ingredient_service.collection.create_index("name", unique=True)
    generic_unit_service.collection.create_index("id", unique=True)
    generic_unit_service.collection.create_index("name", unique=True)
    yield


app = FastAPI(
    title="Meal Planning Backend",
    lifespan=lifespan,
)
app.include_router(router)
