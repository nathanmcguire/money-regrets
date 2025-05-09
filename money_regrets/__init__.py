from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import app as api_app

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/api", api_app)

# Update the StaticFiles mount to use the correct path for the 'site' directory at the project root
app.mount("/docs", StaticFiles(directory="./site"), name="Docs")
