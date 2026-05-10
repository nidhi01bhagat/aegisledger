# AegisLedger

**AI-native distributed financial infrastructure platform** — simulating how modern payment systems like UPI, Stripe, and Razorpay operate internally, with real-time fraud detection, tamper-evident ledger integrity, and an AI finance agent.

> Built to explore: high-throughput payment APIs · graph-based fraud detection · explainable AI · distributed ledger integrity · agentic RAG workflows

---

## The Problem

Modern payment infrastructure fails in predictable, expensive ways:

| Problem | Real-world cost |
|---|---|
| Real-time fraud attacks | ₹2.4T lost annually in India |
| Duplicate transaction execution | Silent double-charges during network retries |
| Ledger tampering | No cryptographic proof of audit history |
| Zero financial insight | Users have data; they have no intelligence |
| Distributed reconciliation failures | Manual correction costs hours per incident |

AegisLedger simulates production-grade solutions to each of these using enterprise backend engineering and AI infrastructure patterns.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   API Gateway                        │
│         FastAPI · JWT · Rate Limiter (Redis)         │
│         Idempotency Keys · Request Validation        │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴─────────────┐
          │                          │
┌─────────▼──────────┐   ┌──────────▼──────────┐
│  Payment Engine    │   │  Fraud Intelligence  │
│  Double-entry      │   │  Velocity scoring    │
│  Atomic transfers  │   │  Graph ring detect   │
│  Merkle audit      │   │  ONNX model serve    │
│  Hash-chain ledger │   │  SHAP explainability │
└─────────┬──────────┘   └──────────┬──────────┘
          │                          │
          └──────────┬───────────────┘
                     │
          ┌──────────▼──────────────┐
          │   Event Stream (Redis   │
          │   Streams / Kafka)      │
          │   Async · Fan-out       │
          └──────────┬──────────────┘
                     │
     ┌───────────────┴───────────────┐
     │                               │
┌────▼───────────┐       ┌───────────▼──────────┐
│  Vector Search │       │  AI Finance Agent     │
│  FAISS HNSW    │       │  LangChain ReAct      │
│  pgvector      │       │  SQL · FAISS · Fraud  │
│  Embeddings    │       │  SSE streaming        │
└────────────────┘       └──────────────────────┘
```

**Request lifecycle:** API Gateway → idempotency check (Redis) → fraud score (< 50ms) → if approved, atomic ledger write (PostgreSQL, double-entry) → Merkle root update → event publish (Redis Streams) → async notification

---

## Core Features

### Payment Infrastructure
- **Idempotent transaction processing** — duplicate payment attempts during retries return the same result, never double-charge
- **Double-entry bookkeeping** — every transfer creates two ledger entries (debit + credit); total always balances
- **Atomic transfer execution** — PostgreSQL transactions with row-level locking; partial writes are impossible
- **Hash-chained ledger** — each record stores `SHA-256(previous_hash + transaction_data)`; tampering breaks the chain

### Fraud Intelligence Engine
- **Velocity-based detection** — sliding window counters in Redis: flags cards with 5+ transactions in 30 seconds
- **Graph-based ring detection** — adjacency graph (device → account → merchant) with BFS traversal to find connected fraud clusters
- **ML risk scoring** — Isolation Forest trained on synthetic data, exported as ONNX, served inline for sub-50ms scoring
- **Explainable flags** — SHAP values explain every flagged transaction in plain English; no black-box decisions

### AI Finance Agent
- **Natural language queries** — ask "show risky transactions today" or "summarize Q1 by merchant"
- **Grounded RAG** — every answer cites specific transaction IDs; hallucination is structurally prevented
- **Tool-calling architecture** — agent selects SQL tool, FAISS retrieval tool, or fraud-check tool based on query type
- **Streaming responses** — SSE stream shows "Thinking → Querying DB → Retrieving..." in real time

### Ledger Integrity
- **Merkle tree batch hashing** — transaction batches stored with a Merkle root; batch verification in O(log n)
- **Append-only architecture** — no UPDATE or DELETE on ledger entries; history is immutable by design
- **Reconciliation engine** — automated batch reconciliation detects discrepancies between expected and actual balances

---

## DSA in Production

This project treats DSA as infrastructure, not interview prep. Every algorithm has a direct business justification.

| Algorithm | Where applied | Business reason |
|---|---|---|
| **Sliding Window** | Redis fraud velocity counter | Detect transaction bursts in bounded time — O(log n) with sorted sets |
| **Hash Map** | Account lookups, idempotency cache | O(1) average retrieval for hot-path transaction processing |
| **Graph + BFS** | Fraud ring detection | Traverse device→account→merchant edges; find clusters of suspicious accounts |
| **Merkle Tree** | Ledger batch integrity | Verify 10,000 transactions in O(log n) comparisons; same structure as Bitcoin |
| **B-Tree Index** | PostgreSQL on (account_id, created_at) | Turn 5-second table scans into 2ms point lookups on 10M+ rows |
| **HNSW Graph** | FAISS vector search | Approximate nearest neighbour in O(log n) — hierarchical navigable small world |
| **Queue / Stream** | Redis Streams event pipeline | Decouple payment processing from fraud analysis; async fan-out to consumers |

---

## Distributed Ledger Design

AegisLedger explores blockchain-inspired patterns for financial trust — without speculative cryptocurrency applications.

**Why this matters:** UPI, NPCI settlement systems, and enterprise financial platforms use distributed ledger concepts for exactly the same reasons: auditability, tamper-evidence, and reconciliation reliability.

### Hash-Chained Records
```
Block N-1                    Block N                      Block N+1
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│ txn_data     │            │ txn_data     │            │ txn_data     │
│ prev_hash: 0 │──SHA-256──▶│ prev_hash:   │──SHA-256──▶│ prev_hash:   │
│ hash: abc123 │            │   abc123     │            │   def456     │
└──────────────┘            │ hash: def456 │            │ hash: ghi789 │
                            └──────────────┘            └──────────────┘
```
Modify any record → its hash changes → every subsequent hash breaks → tamper is immediately detectable.

### Merkle Batch Verification
Each settled batch stores a Merkle root. Auditors can verify the integrity of any transaction in the batch with O(log n) hash comparisons — not a full table scan.

### Future: Raft Consensus Simulation
Planned simulation of distributed settlement coordination using Raft consensus, demonstrating leader election and log replication under node failure scenarios.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| API | FastAPI (async) | High-throughput async I/O; automatic OpenAPI docs |
| Database | PostgreSQL | ACID guarantees, row-level locking, B-tree indexes, pgvector |
| Cache + Streams | Redis | Sub-millisecond velocity counters, idempotency store, event fan-out |
| ML Serving | ONNX Runtime | Language-agnostic model serving; Isolation Forest → ONNX in 10 lines |
| Vector Search | FAISS (HNSW) + pgvector | In-memory ANN for low latency; pgvector for persistence |
| AI Orchestration | LangChain + LangGraph | ReAct agent with tool calling; structured reasoning loops |
| Event Streaming | Redis Streams (Kafka planned) | Async decoupling of payment and fraud processing |
| Containerisation | Docker + docker-compose | One-command local environment; consistent across machines |
| Observability | OpenTelemetry + Grafana | Trace every request; p50/p95/p99 per endpoint |

---

## Performance Benchmarks

> Measured on: MacBook M2 Pro, 16GB RAM, Docker local environment, 100K synthetic transactions

| Metric | Result | Method |
|---|---|---|
| Payment API p99 latency | < 15ms | k6 load test, 1000 concurrent users |
| Fraud scoring latency | < 50ms | Redis velocity + ONNX inference measured end-to-end |
| FAISS HNSW recall@10 | 96.2% | Compared against brute-force IndexFlatL2 baseline |
| RAG retrieval p95 | < 280ms | LangChain retrieval step, measured with OpenTelemetry |
| Ledger write throughput | ~3,400 TPS | PostgreSQL with connection pooling (PgBouncer) |
| Merkle batch verification | O(log n) | 10,000-transaction batch verified in < 5ms |

---

## Quickstart

```bash
# 1. Clone and configure
git clone https://github.com/yourusername/aegisledger.git
cd aegisledger
cp .env.example .env  # add your OpenAI API key

# 2. Start all services
docker-compose up -d

# 3. Run database migrations
docker-compose exec api alembic upgrade head

# 4. Try the API
curl -X POST http://localhost:8000/api/v1/transfers \
  -H "Authorization: Bearer <token>" \
  -H "X-Idempotency-Key: unique-key-001" \
  -H "Content-Type: application/json" \
  -d '{"from_account": "acc_001", "to_account": "acc_002", "amount": 500.00}'

# 5. Ask the AI agent
curl -X POST http://localhost:8000/api/v1/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the top 5 merchants by transaction volume this week"}'
```

---

## Project Structure

```
aegisledger/
├── api/
│   ├── routes/           # FastAPI routers: transfers, fraud, agent
│   ├── middleware/        # JWT auth, rate limiting, idempotency
│   └── dependencies/      # DB sessions, Redis client, auth
├── core/
│   ├── ledger/           # Double-entry engine, Merkle tree, hash chain
│   ├── fraud/            # Velocity checks, graph traversal, ONNX serving
│   └── reconciliation/   # Batch settlement, discrepancy detection
├── ai/
│   ├── agent/            # LangGraph ReAct agent, tool definitions
│   ├── rag/              # Ingestion pipeline, chunking, retrieval
│   └── embeddings/       # Transaction feature vectors, FAISS index
├── infra/
│   ├── events/           # Redis Streams producers and consumers
│   └── observability/    # OpenTelemetry setup, Prometheus metrics
├── tests/
│   ├── unit/             # Algorithm unit tests with timing assertions
│   └── integration/      # End-to-end payment and fraud scenarios
├── docker-compose.yml
├── alembic/              # Database migrations
└── docs/
    ├── architecture.md   # Full system design with diagrams
    ├── dsa-in-production.md   # Algorithm decisions documented
    └── benchmarks.md     # Load test results with methodology
```

---

## Case Studies

Deep dives on design decisions made in this project:

- **[How I built a Merkle-tree ledger for tamper-evident financial records](#)** — Medium
- **[FAISS HNSW explained: tuning M and ef for financial transaction search](#)** — Medium
- **[Velocity-based fraud detection: from sliding window algorithm to Redis implementation](#)** — Medium
- **[Why I chose ONNX over pickle for ML model serving in a payment API](#)** — Medium

---

## Fellowship + Research Relevance

This project directly applies to infrastructure challenges studied by:

- **NPCI** — Merkle ledger integrity, distributed settlement reconciliation, UPI-style payment orchestration
- **Razorpay Engineering** — idempotent payment APIs, velocity fraud detection, event-driven architecture
- **Stripe Research** — explainable AI fraud scoring, agentic financial workflows, compliance-aware reasoning
- **Visa Innovation** — graph-based fraud ring detection, low-latency risk scoring, distributed trust models

---

## What I Learned / Engineering Decisions

Brief notes on non-obvious choices made during the build:

**Why HNSW over IVF in FAISS?** IVF requires a training phase and struggles with small datasets. HNSW builds incrementally, has better recall at low ef values, and handles the dataset sizes relevant to single-merchant transaction histories better. Benchmark comparison in `docs/benchmarks.md`.

**Why double-entry instead of single balance column?** A single balance column requires a `SELECT → compute → UPDATE` that creates race conditions under concurrent transactions. Double-entry with INSERT-only rows is safe under PostgreSQL's MVCC without application-level locking.

**Why ONNX for the fraud model?** Pickle-serialised sklearn models are version-dependent and slow to load. ONNX runtime loads in < 100ms, runs on CPU and GPU without code changes, and the same model file works across Python, Rust, and Go.

---

## Roadmap

- [x] Payment API with idempotency and rate limiting
- [x] Double-entry ledger with hash-chain integrity
- [x] Velocity-based fraud detection (Redis sliding window)
- [x] Graph fraud ring detection (BFS on adjacency graph)
- [x] ONNX fraud model serving with SHAP explanations
- [x] FAISS HNSW vector search + pgvector persistence
- [x] LangChain ReAct agent with SQL + FAISS + fraud tools
- [x] Agentic RAG with grounded retrieval and confidence scores
- [ ] Kafka migration for event streaming (Redis Streams → Kafka)
- [ ] Raft consensus simulation for distributed settlement
- [ ] Graph Neural Network fraud model (upgrade from Isolation Forest)
- [ ] NeMo Guardrails for compliance-aware agent responses

---

## Contributions

Issues and PRs are welcome — especially around:
- Performance improvements to the FAISS indexing pipeline
- Additional fraud detection heuristics
- Alternative consensus algorithm implementations

See `CONTRIBUTING.md` for guidelines.

---

*Built as a deep-dive into production financial infrastructure engineering. Every design decision documented. Every algorithm benchmarked.*