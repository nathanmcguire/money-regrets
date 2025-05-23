# main.py - Entry point for the Money Regrets API backend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .plaid import plaid_router
from .users import users_router

# Create the main FastAPI app
app = FastAPI(version="1.0.0")

# Apply CORS middleware to both the main app and the v1 sub-app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plaid_router, prefix="/plaid")
app.include_router(users_router, prefix="/users")
