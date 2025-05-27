# Accounts

## Account Transactions

1. account_transactions (raw import)
Immutable raw input from financial institutions:

sql
Copy
Edit
id (PK)
integration_id (FK)
external_id
account_id (FK to imported account)
amount
date
description
raw_data (JSON or blob)
imported_at
✅ Never update once inserted.

