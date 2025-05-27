from typing import Optional, Literal
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class PlaidLinkToken(BaseModel):
    link_token: str


class PlaidAccount(SQLModel, table=True):
    __tablename__ = "plaid_accounts"

    item_id: str = Field(primary_key=True)
    account_id: str = Field(primary_key=True)
    mask: Optional[str] = None
    name: Optional[str] = None
    official_name: Optional[str] = None
    subtype: Optional[str] = None
    type: Optional[str] = None


class PlaidItem(SQLModel, table=True):
    __tablename__ = "plaid_items"

    item_id: str = Field(primary_key=True)
    access_token: Optional[str] = None  # Store securely, never send to client
    available_products: Optional[str] = None  # Store as comma-separated string or JSON
    billed_products: Optional[str] = None     # Store as comma-separated string or JSON
    error: Optional[str] = None
    institution_id: Optional[str] = None
    webhook: Optional[str] = None


class PlaidTransaction(SQLModel, table=True):
    __tablename__ = "plaid_transactions"

    transaction_id: str = Field(primary_key=True)
    account_id: Optional[str] = None
    account_owner: Optional[str] = None
    amount: Optional[str] = None
    category: Optional[str] = None  # Store as comma-separated string or JSON
    category_id: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None  # Store as JSON string
    name: Optional[str] = None
    payment_meta: Optional[str] = None  # Store as JSON string
    pending: Optional[str] = None
    pending_transaction_id: Optional[str] = None
    transaction_type: Optional[str] = None


class PlaidBalance(SQLModel, table=True):
    __tablename__ = "plaid_balances"

    id: str = Field(primary_key=True)
    account_id: Optional[str] = None
    timestamp: Optional[str] = None
    available: Optional[str] = None
    current: Optional[str] = None
    limit: Optional[str] = None


class PlaidItemPublicToken(BaseModel):
    public_token: str
    environment: Literal["sandbox", "production"] = "sandbox"
