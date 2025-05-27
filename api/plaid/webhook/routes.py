import hashlib
import hmac
import time
import requests
from jose import jwt
import json
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Response, status, Depends, Body
from sqlmodel import Session
from api.database import get_session
from .models import PlaidWebhook, PlaidWebhookEvent
import os

WEBHOOK_VERIFICATION_ENDPOINT = 'https://production.plaid.com/webhook_verification_key/get'
CACHED_KEY = None

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "your_client_id")
PLAID_PRODUCTION_SECRET = os.getenv("PLAID_PRODUCTION_SECRET", "your_production_secret")

webhook_router = APIRouter()


def verify_plaid_webhook(body: str, headers: dict) -> bool | int:
    global CACHED_KEY
    signed_jwt = headers.get('plaid-verification')
    if not signed_jwt:
        return 401
    try:
        current_key_id = jwt.get_unverified_header(signed_jwt)['kid']
    except Exception:
        return 401
    if CACHED_KEY is None:
        response = requests.post(WEBHOOK_VERIFICATION_ENDPOINT, json={
            'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_PRODUCTION_SECRET,
            'key_id': current_key_id
        })
        if response.status_code != 200:
            return 401
        CACHED_KEY = response.json()['key']
    if CACHED_KEY is None:
        return 401
    try:
        claims = jwt.decode(signed_jwt, CACHED_KEY, algorithms=['ES256'])
    except Exception:
        return 401
    if claims.get('iat', 0) < time.time() - 5 * 60:
        return 425
    m = hashlib.sha256()
    m.update(body.encode())
    body_hash = m.hexdigest()
    if not hmac.compare_digest(body_hash, claims.get('request_body_sha256', '')):
        return 401
    return 204


@webhook_router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Webhook received and logged successfully."},
        401: {"description": "Plaid webhook verification failed."},
        425: {"description": "Webhook is too old (received 5+ minutes after iat)."}
    }
)
async def receive_webhook(
    request: Request,
    session: Session = Depends(get_session),
    body: PlaidWebhookEvent = Body(..., description="Plaid webhook payload")
):
    body_str = body.json()
    headers = dict(request.headers)
    result = verify_plaid_webhook(body_str, headers)
    if result == 401:
        raise HTTPException(status_code=401, detail="Plaid webhook verification failed.")
    if result == 425:
        raise HTTPException(status_code=425, detail="Webhook is too old (received 5+ minutes after iat).")
    webhook = PlaidWebhook(
        body=body_str,
        headers=json.dumps(headers),
        received_at=datetime.utcnow(),
        processed=True,
        processing_error=None
    )
    session.add(webhook)
    session.commit()
    return Response(status_code=204)
