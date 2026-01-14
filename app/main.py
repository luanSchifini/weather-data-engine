from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="GnTech Weather API Escalável",
    lifespan=lifespan
)

app.include_router(api_router)


@app.get("/health", tags=["Monitoring"])
def health():
    return {"status": "ok"}

