import os
import plaid
from plaid.api import plaid_api
from fastapi import APIRouter
from .models import PlaidLinkToken, PlaidItem, PlaidItemPublicToken
from sqlmodel import Session
from fastapi import Depends
from api.database import get_session
from .webhook import webhook_router
import hashlib
import hmac
import time
import requests
from jose import jwt
from fastapi import Request, HTTPException, Response, status
import json
from datetime import datetime
from fastapi import Body

# Plaid credentials (set these as environment variables in production)
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "your_client_id")
PLAID_SANDBOX_SECRET = os.getenv("PLAID_SANDBOX_SECRET", "your_sandbox_secret")
PLAID_PRODUCTION_SECRET = os.getenv("PLAID_PRODUCTION_SECRET", "your_production_secret")

# Plaid API client setup for sandbox
sandbox_configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SANDBOX_SECRET,
    }
)
sandbox_api_client = plaid.ApiClient(sandbox_configuration)
sandbox_client = plaid_api.PlaidApi(sandbox_api_client)

# Plaid API client setup for production
production_configuration = plaid.Configuration(
    host=plaid.Environment.Production,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_PRODUCTION_SECRET,
    }
)
production_api_client = plaid.ApiClient(production_configuration)
production_client = plaid_api.PlaidApi(production_api_client)

plaid_router = APIRouter(tags=["Plaid"])

plaid_router.include_router(webhook_router, prefix="/webhook")
# Webhook verification endpoint


@plaid_router.get("/link/token", response_model=PlaidLinkToken)
def create_link_token_get(production: bool = False):
    plaid_client = production_client if production else sandbox_client
    request_data = {
        "user": {"client_user_id": "ReplceMeWithLoggedInUserID"},
        "client_name": "Money Regrets",
        "products": ["transactions"],
        "country_codes": ["US"],
        "language": "en"
    }
    response = plaid_client.link_token_create(request_data)
    return PlaidLinkToken(
        link_token=response["link_token"]
    )


@plaid_router.post("/item/public-token", status_code=status.HTTP_204_NO_CONTENT)
def exchange_item_public_token(request: PlaidItemPublicToken, session: Session = Depends(get_session)):
    environment = request.environment
    public_token = request.public_token
    plaid_client = sandbox_client if environment == "sandbox" else production_client
    response = plaid_client.item_public_token_exchange({"public_token": public_token})
    item_id = response["item_id"]
    access_token = response["access_token"]
    # Create or update PlaidItem in the database
    plaid_item = session.get(PlaidItem, item_id)
    if plaid_item:
        plaid_item.error = None
    else:
        plaid_item = PlaidItem(item_id=item_id)
        session.add(plaid_item)
    # Store access_token securely in your database here (not returned to client)
    plaid_item.access_token = access_token
    session.commit()
    return Response(status_code=204)

# (Plaid webhook logic and endpoint moved to webhooks/routes.py)
