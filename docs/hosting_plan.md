# 🗂️ Hosting Plan – Money Regrets

## 🌐 Domains

| Domain                | Purpose                |
|---------------------- |------------------------|
| moneyregrets.com      | Marketing site         |
| docs.                 | Documentation          |
| app.                  | Frontend App           |
| api.                  | Backend API (FastAPI)  |
| www.                  | Redirects to apex      |

> **Note:** The `www` subdomain should be configured to redirect to the apex domain (`moneyregrets.com`). This is still a best practice for SEO and user experience, ensuring all traffic is consolidated to a single canonical domain.

## 🧱 Infrastructure Stack

| Layer         | Tech                        | Host                                    |
|-------------- |---------------------------- |-----------------------------------------|
| Frontend App  | React (Next.js)             | Vercel                                  |
| Marketing Site| Next.js (separate or same)  | Vercel                                  |
| API Backend   | FastAPI + Uvicorn/Gunicorn  | Fly.io / Railway / DO App Platform / Azure |
| Database      | PostgreSQL / Supabase       | Supabase / Railway / DO Managed DB      |
| Auth          | Clerk / Auth0 / Supabase Auth| SaaS or same as DB                     |
| Storage       | S3-compatible (uploads)     | Cloudflare R2 / Supabase Storage        |
| DNS           | Cloudflare                  | Free, fast, good SSL support            |

## 🪄 Deployment Flow
- **Marketing + App:** Git push → Vercel deploys automatically
- **API:** Docker deploy or git push to Railway/Fly/etc.
- **DB Backups:** Daily backups with provider or `pg_dump` to object storage
- **Monitoring:** Upptime / BetterStack / Sentry

## 🔐 Security + Best Practices
- ✅ SSL/TLS via Cloudflare or native
- ✅ HTTP headers hardened (helmet, Vercel config)
- ✅ Rate limiting on API endpoints
- ✅ CAPTCHA on public forms
- ✅ Audit trail on sign-ins (for pros feature)

## 🔄 Dev → Staging → Prod Flow (optional)

| Env      | Purpose          | Hosting                                 |
|----------|------------------|-----------------------------------------|
| dev.     | Personal sandbox | Vercel Preview                          |
| staging. | Team testing     | Vercel Preview / Fly.io staging app     |
| prod     | Live users       | moneyregrets.com, app.moneyregrets.com  |
