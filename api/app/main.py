from fastapi import FastAPI
from app.core.settings import settings
from app.routers.extract import router as extract_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")

app.include_router(extract_router, prefix="/api/v1", tags=["Extract Text"])