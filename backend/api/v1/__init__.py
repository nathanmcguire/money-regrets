from fastapi import FastAPI
from .users import router as users_router

app = FastAPI(version="1.0.0")

app.include_router(users_router, prefix="/users", tags=["Users"])