from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.resources.endpoints import generic_unit_service, ingredient_service, router


@asynccontextmanager
async def lifespan(_: FastAPI):
    ingredient_service.collection.create_index("id", unique=True)
    generic_unit_service.collection.create_index("id", unique=True)
    yield


app = FastAPI(
    title="Meal Planning Backend",
    lifespan=lifespan,
)
app.include_router(router)
