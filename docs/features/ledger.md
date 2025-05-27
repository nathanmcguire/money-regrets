# Ledger

An account ledger is the account-specific aggregation of all journal entries affecting that account, with a running balance.

The general ledger is the complete record of all financial transactions combining the account ledgers for every account. It provides a comprehensive view of all debits and credits, enabling accurate financial reporting and reconciliation across the entire system.

## 🏗️ Suggested View: ledger_entries
You can generate this via SQL or ORM as a derived view.

sql
Copy
Edit
SELECT
  a.id AS account_id,
  a.name AS account_name,
  j.date,
  j.description,
  e.amount,
  e.entry_type,
  CASE 
    WHEN e.entry_type = 'debit' THEN e.amount
    ELSE -e.amount
  END * CASE
    WHEN a.type IN ('asset', 'expense') THEN 1
    ELSE -1
  END AS impact,
  SUM(...) OVER (PARTITION BY a.id ORDER BY j.date, j.id) AS running_balance,
  j.id AS journal_transaction_id
FROM
  journal_entries e
JOIN
  journal_transactions j ON e.journal_transaction_id = j.id
JOIN
  accounts a ON e.account_id = a.id
ORDER BY
  a.id, j.date;

📊 What Can You Do With the Ledger?
Show per-account statements (like your bank does)

Calculate net worth (total assets – total liabilities)

Track budget variance against actuals

Reconcile imported vs. journaled transactions

Provide drilldowns from summary charts into ledger lines

💡 Optional Enhancement
Create a materialized view or a cached table like:

sql
Copy
Edit
ledger_snapshots (
  account_id,
  date,
  balance
)
To make balance lookups fast for reports, dashboards, and net worth tracking without recalculating live.