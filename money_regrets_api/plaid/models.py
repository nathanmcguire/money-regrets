from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


class PlaidLinkTokenRequest(BaseModel):
    user_id: str


class PlaidLinkTokenResponse(BaseModel):
    link_token: str


Base = declarative_base()


class PlaidAccount(Base):
    __tablename__ = "plaid_accounts"

    item_id = Column(String, primary_key=True)
    account_id = Column(String, primary_key=True)
    mask = Column(String)
    name = Column(String)
    official_name = Column(String)
    subtype = Column(String)
    type = Column(String)


class PlaidItem(Base):
    __tablename__ = "plaid_items"

    item_id = Column(String, primary_key=True)
    available_products = Column(String)  # Store as comma-separated string or JSON
    billed_products = Column(String)     # Store as comma-separated string or JSON
    error = Column(String)
    institution_id = Column(String)
    webhook = Column(String)


class PlaidTransaction(Base):
    __tablename__ = "plaid_transactions"

    transaction_id = Column(String, primary_key=True)
    account_id = Column(String)
    account_owner = Column(String, nullable=True)
    amount = Column(String)
    category = Column(String)  # Store as comma-separated string or JSON
    category_id = Column(String)
    date = Column(String)
    location = Column(String)  # Store as JSON string
    name = Column(String)
    payment_meta = Column(String)  # Store as JSON string
    pending = Column(String)
    pending_transaction_id = Column(String, nullable=True)
    transaction_type = Column(String)


class PlaidBalance(Base):
    __tablename__ = "plaid_balances"

    id = Column(String, primary_key=True)
    account_id = Column(String)
    timestamp = Column(String)
    available = Column(String)
    current = Column(String)
    limit = Column(String)