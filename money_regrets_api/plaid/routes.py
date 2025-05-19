import os
import plaid
from plaid.api import plaid_api
from fastapi import APIRouter, Query
from .models import PlaidLinkTokenRequest, PlaidLinkTokenResponse

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


@plaid_router.post("/link/token", response_model=PlaidLinkTokenResponse)
def create_plaid_link_token(request: PlaidLinkTokenRequest, environment: str = Query("sandbox", enum=["sandbox", "production"])):
    plaid_client = sandbox_client if environment == "sandbox" else production_client
    request_data = {
        "user": {"client_user_id": request.user_id},
        "client_name": "Money Regrets App",
        "products": ["auth", "transactions"],
        "country_codes": ["US"],
        "language": "en"
    }
    response = plaid_client.link_token_create(request_data)
    return PlaidLinkTokenResponse(link_token=response["link_token"])
