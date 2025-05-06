from fastapi import APIRouter
from backend.routers.user import router as user_router

# Create a main router to include all sub-routers
router = APIRouter()


# Root endpoint
@router.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


# Include individual routers
router.include_router(user_router)
