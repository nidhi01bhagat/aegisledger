# PostgreSQL Database Setup — AegisLedger

## Overview

This document explains how PostgreSQL was configured for the AegisLedger backend infrastructure.

The database layer is responsible for storing:

- users
- financial accounts
- transfers
- ledger entries
- fraud metadata
- AI retrieval metadata

---

# Why PostgreSQL?

PostgreSQL was selected because it provides:

- ACID transaction guarantees
- strong relational consistency
- indexing support
- transactional rollback safety
- enterprise-grade reliability

These properties are critical for financial systems where correctness and consistency are mandatory.

---

# pgAdmin Setup

pgAdmin was used as the database administration interface.

The PostgreSQL service was verified through:

Windows Services → postgresql-x64-13

---

# Database Creation

Database Name:

```text
aegisledger_db
```

The database was created using:

pgAdmin → Databases → Create → Database

---

# Environment Configuration

Environment variables were configured using:

```env
DATABASE_URL=postgresql://postgres:%23Rosh0112@localhost:5432/aegisledger_db
```

Special characters in passwords were URL-encoded.

Example:

| Character | Encoded |
|----------|----------|
| # | %23 |

---

# Engineering Concepts Learned

## ACID Transactions

Ensures:
- atomicity
- consistency
- isolation
- durability

Critical for payment correctness.

---

## Connection Management

SQLAlchemy engine + session management will later handle:

- transaction lifecycle
- rollback
- commit
- concurrency safety

---

## Security Practices

Sensitive credentials are stored inside:

```text
.env
```

and excluded from Git tracking using:

```text
.gitignore
```

---

# Next Steps

- SQLAlchemy integration
- ORM model creation
- double-entry ledger modeling
- transactional payment execution