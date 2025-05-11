from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .v1 import app as v1_app

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/v1", v1_app)
