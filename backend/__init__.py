from fastapi import FastAPI
import os

from backend.routers import router as api_router


# Initialize FastAPI app
app = FastAPI()


# Include the centralized router
app.include_router(api_router)



