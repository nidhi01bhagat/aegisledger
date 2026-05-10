# Database Connection Architecture — AegisLedger

# Overview

This document explains how the AegisLedger backend connects to PostgreSQL using SQLAlchemy ORM and environment-based configuration management.

The database connection layer is one of the most important foundational components in enterprise backend systems because every critical workflow — users, accounts, transfers, ledger entries, fraud events, and AI metadata — depends on reliable database communication.

---

# Why PostgreSQL Was Selected

PostgreSQL was chosen because it provides enterprise-grade transactional guarantees required for financial infrastructure systems.

Key advantages:

* ACID transaction guarantees
* strong relational consistency
* rollback safety
* indexing support
* concurrency handling
* scalability
* mature ecosystem

Financial systems require correctness over convenience. PostgreSQL is widely used in banking, fintech, and distributed financial systems because it prioritizes transactional integrity and reliability.

---

# Database Connection Flow

```text
FastAPI Application
        ↓
SQLAlchemy ORM
        ↓
PostgreSQL Driver
        ↓
PostgreSQL Database
```

The backend application communicates with PostgreSQL through SQLAlchemy, which acts as an abstraction layer between Python objects and SQL queries.

---

# Why SQLAlchemy ORM Was Used

## What is an ORM?

ORM stands for:

```text
Object Relational Mapper
```

An ORM allows developers to work with database entities as Python objects instead of writing raw SQL queries everywhere.

Example:

Instead of manually writing:

```sql
SELECT * FROM users;
```

we can write:

```python
db.query(User).all()
```

---

# Why ORM Is Important in Enterprise Systems

## 1. Cleaner Code Structure

ORMs separate:

* business logic
* database logic

This improves:

* maintainability
* readability
* onboarding

Large engineering teams rarely place raw SQL everywhere inside application code because it becomes difficult to maintain at scale.

---

## 2. Schema Modeling

ORMs allow backend engineers to define tables as structured Python models.

Example:

```python
class User(Base):
    __tablename__ = "users"
```

This creates a clear mapping between:

* database tables
* backend entities

This improves architecture clarity.

---

## 3. Relationship Management

ORMs simplify:

* foreign keys
* one-to-many relationships
* joins
* relational integrity

This is extremely important for:

* financial accounts
* transaction ownership
* ledger relationships

---

## 4. Transaction Management

SQLAlchemy provides session-based transaction handling.

This becomes critical later for:

* rollback handling
* atomic payment execution
* concurrency safety

Example:

```python
db.commit()
db.rollback()
```

Financial systems cannot tolerate partial failures.

Either:

* everything succeeds
  OR
* everything rolls back

---

## 5. Database Portability

ORMs abstract database-specific implementations.

This means:
PostgreSQL could later be replaced or extended without rewriting the entire backend logic layer.

---

# SQLAlchemy Engine

The SQLAlchemy engine is responsible for managing the connection between the FastAPI backend and PostgreSQL.

Implementation:

```python
engine = create_engine(DATABASE_URL)
```

The engine:

* opens database connections
* manages connection pooling
* executes SQL operations internally

---

# Why Connection Pooling Matters

Enterprise systems cannot create a new DB connection for every request because connection creation is expensive.

Connection pooling:

* reuses active DB connections
* improves latency
* reduces overhead
* increases throughput

This becomes very important under:

* high transaction load
* concurrent requests
* distributed workloads

---

# Session Management

A database session represents a transactional interaction with the database.

Implementation:

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

---

# Why Sessions Are Important

Sessions help manage:

* transaction lifecycle
* rollback handling
* consistency
* isolation

Every financial operation should execute inside a controlled transactional boundary.

Example:

```text
Transfer Begins
    ↓
Debit Sender
    ↓
Credit Receiver
    ↓
Create Ledger Entry
    ↓
Commit
```

If any step fails:

```text
Rollback Entire Transaction
```

This guarantees financial correctness.

---

# Why autocommit=False Was Used

Automatic commits are dangerous in financial systems.

We want explicit control over:

* when data is committed
* when rollback occurs

This prevents inconsistent transaction states.

---

# Why autoflush=False Was Used

Autoflush automatically synchronizes pending changes with the database.

Disabling autoflush gives:

* better transaction control
* predictable execution order
* safer financial workflows

---

# Base Class Architecture

Implementation:

```python
Base = declarative_base()
```

The Base class acts as the parent class for all ORM models.

Example:

```python
class User(Base):
```

This standardizes:

* schema generation
* model registration
* metadata handling

All future entities:

* users
* accounts
* transfers
* ledger entries

inherit from this common base.

---

# Environment Variable Configuration

Database credentials are stored inside:

```text
.env
```

instead of directly inside source code.

Example:

```env
DATABASE_URL=postgresql://postgres:%23Rosh0112@localhost:5432/aegisledger_db
```

---

# Why Environment Variables Are Important

## 1. Security

Sensitive credentials should never be hardcoded into source files.

Hardcoding passwords creates major security risks:

* accidental GitHub leaks
* credential exposure
* production compromise

---

## 2. Environment Separation

Different environments require different configurations.

Example:

| Environment | Database   |
| ----------- | ---------- |
| local       | localhost  |
| staging     | staging DB |
| production  | cloud DB   |

Environment variables make configuration flexible.

---

## 3. Deployment Compatibility

Cloud systems:

* Docker
* Kubernetes
* AWS
* GCP

all heavily depend on environment-based configuration management.

---

# Why .env Is Added To .gitignore

The `.env` file contains:

* database credentials
* API keys
* sensitive infrastructure configuration

It must never be pushed to GitHub.

`.gitignore` prevents accidental exposure.

---

# Engineering Concepts Learned

This phase introduced several enterprise backend engineering concepts:

| Concept               | Importance                |
| --------------------- | ------------------------- |
| ORM                   | scalable backend modeling |
| Sessions              | transactional correctness |
| Connection pooling    | performance optimization  |
| Environment variables | secure configuration      |
| PostgreSQL            | financial consistency     |
| Rollback handling     | payment safety            |
| Relational modeling   | structured financial data |

---

# Relevance To Financial Infrastructure

This database architecture forms the foundation for:

* account systems
* transaction processing
* fraud analysis
* ledger integrity
* AI retrieval metadata
* auditability
* distributed financial workflows

Without reliable database infrastructure, payment systems cannot guarantee:

* correctness
* trust
* consistency
* integrity

---

# Next Steps

The next engineering phase focuses on:

* user entity modeling
* account system design
* transfer workflows
* double-entry ledger implementation
* idempotent payment handling
* atomic financial transactions
