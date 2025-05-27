
# Reconciliation


## 🔄 Conceptual Roles
Concept	Purpose
AccountTransactions	Raw, imported data (e.g. from Plaid, OFX, CSV). Immutable.
JournalTransaction	Canonical, clean double-entry transactions used for your ledger.
JournalEntry	Individual debit/credit lines linked to accounts and a JournalTransaction.
Mapping Layer	Associates imported AccountTransactions to JournalTransactions.



## 🧭 Reconciliation Strategy
The import layer never gets modified—you treat it as read-only and append-only.

You allow your users or reconciliation logic to create new journal_transactions, selecting from the account_transactions pool.

The journal_transaction_links allow you to:

Trace back every journal entry to original source data

Detect if an account_transaction has been reconciled (via EXISTS on the link table)

Manage exception cases (e.g., duplicates, splits, partial payments)