from fastapi import FastAPI
from configuration import environment
from configuration.logger import get_logger

logger = get_logger(__name__)
settings = environment.get_config()
app = FastAPI(title=settings.application_name)

@app.get("/")
async def home():
    return {"title": "Hello World", "test":"ok"}


@app.get("/test")
async def home():
    return {"title": "Hello World Test", "test":"ok"}