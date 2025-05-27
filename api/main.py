# main.py - Entry point for the Money Regrets API backend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.plaid import plaid_router
from api.users import users_router
from api.walmart import walmart_router

# Create the main FastAPI app
app = FastAPI(version="1.0.0")

# Apply CORS middleware to allow requests from your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # No "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plaid_router, prefix="/plaid")
app.include_router(users_router, prefix="/users")
app.include_router(walmart_router, prefix="/walmart")
