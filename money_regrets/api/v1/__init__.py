from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from .users import router as users_router

app = FastAPI(version="1.0.0")

app.include_router(users_router, prefix="/users", tags=["Users"])

# Mount MkDocs static files
docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'site')
app.mount('/docs', StaticFiles(directory=docs_path), name='docs')

# Ensure a newline at the end of the file
