from fastapi import FastAPI
from app.database import engine, Base
from app.api.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GnTech Weather API Escalável")

app.include_router(api_router)


@app.get("/health", tags=["Monitoring"])
def health():
    return {"status": "ok"}
