from pydantic import BaseModel


class PlaidLinkTokenRequest(BaseModel):
    user_id: str


class PlaidLinkTokenResponse(BaseModel):
    link_token: str
