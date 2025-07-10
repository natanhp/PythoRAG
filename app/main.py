from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.collection_loader import init_qdrant


from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    await init_qdrant(app)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    router,
    prefix="/api",
)
