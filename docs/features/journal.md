# Journal

📓 In modern accounting, a journal is:
A chronological record of all financial transactions, before they are posted to the general ledger.

This structure is core to double-entry bookkeeping, where each entry:

Has a date

A description

At least one debit

At least one credit

Ensures that total debits equal total credits

## 🧱 Why the name still matters in modern apps
Using the term journal_transaction instead of just transaction helps convey:

Formal posting:
It’s not just an API-pulled line item or a bank feed. It’s a formally accepted and balanced record in your accounting system.

Chronological order:
Journals are always recorded in order of occurrence. This matters for audit trails and historical tracing.

Batching or grouping:
A journal_transaction can group multiple external inputs into one logical business event (e.g., payroll, daily sales summary, bank reconciliation).

## 🔁 Journal vs Ledger

Term	Purpose	Example
Journal	Temporary, chronological recording of events	"On 5/23, received $100 from customer"
Ledger	Final account balances per account	"Cash account has $2,350 balance"

You journal first → then post to the ledger.


## Journal Transactions

2. journal_transactions
Finalized, balanced transactions representing the ledger.

sql
Copy
Edit
id (PK)
description
date
reference_number
created_by
created_at
This is where double-entry happens.

## Journal Transaction Links
4. journal_transaction_links (association table)
Maps imported transactions to reconciled journal entries without mutating the source.

sql
Copy
Edit
id (PK)
journal_transaction_id (FK)
account_transaction_id (FK)
note (optional)
linked_at
This preserves a clear audit trail and allows partial matches (e.g., multiple account_transactions mapping to one journal_transaction, like split deposits).


## Journal Entries

3. journal_entries
Each line item for the transaction: debit or credit to an account.

sql
Copy
Edit
id (PK)
journal_transaction_id (FK)
ledger_account_id (FK to your internal accounts)
entry_type (ENUM: debit, credit)
amount
memo
🔄 Balancing logic ensures total debits = total credits per journal_transaction_id.