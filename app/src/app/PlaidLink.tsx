"use client";

import React, { useCallback, useEffect, useState } from 'react';
import Script from 'next/script';

export default function PlaidLink() {
  const [linkToken, setLinkToken] = useState<string | null>(null);
  const [plaidLoaded, setPlaidLoaded] = useState(false);

  useEffect(() => {
    async function createLinkToken() {
      const res = await fetch('http://localhost:8000/plaid/link/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'unique-user-id', environment: 'sandbox' })
      });
      const data = await res.json();
      setLinkToken(data.link_token);
    }
    createLinkToken();
  }, []);

  const onSuccess = useCallback((public_token: string, metadata: any) => {
    // Align with PlaidItemPublicTokenRequest and PlaidItemPublicTokenResponse models
    const requestBody: { public_token: string; environment: 'sandbox' | 'production' } = {
      public_token,
      environment: 'sandbox',
    };
    fetch('http://localhost:8000/plaid/item/public-token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    })
      .then(res => res.json())
      .then((data: { item_id: string; environment: 'sandbox' | 'production' }) => {
        if (data.item_id) {
          alert(`Plaid Link Success!\nItem ID: ${data.item_id}`);
        } else {
          alert('Plaid Link Error: Unexpected response from server.');
        }
      })
      .catch(err => {
        alert('Plaid Link Error: ' + err.message);
      });
  }, []);

  useEffect(() => {
    if (!linkToken || !plaidLoaded) return;
    // @ts-ignore
    const handler = window.Plaid.create({
      token: linkToken,
      onSuccess,
    });
    const btn = document.getElementById('plaid-link-btn');
    if (btn) {
      btn.addEventListener('click', () => handler.open());
      return () => btn.removeEventListener('click', () => handler.open());
    }
    return () => handler.destroy();
  }, [linkToken, onSuccess, plaidLoaded]);

  return (
    <>
      <Script
        src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"
        strategy="afterInteractive"
        onLoad={() => setPlaidLoaded(true)}
      />
      <button id="plaid-link-btn" disabled={!linkToken || !plaidLoaded} style={{ padding: 12, fontSize: 18 }}>
        Connect Bank with Plaid
      </button>
    </>
  );
}
