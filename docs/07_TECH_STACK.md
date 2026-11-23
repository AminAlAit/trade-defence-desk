# 07 Tech stack

Fewer tools, each one used for real. Most come from the bootcamp.

## The stack, by what each layer does for the story

| Layer | Tool | What it does here | Lane |
|---|---|---|---|
| Language and packages | Python 3.13, `uv` | everything is Python; `uv` installs the same versions for everyone | A |
| Code quality | `ruff`, `ty`, `pytest` | style, type and behaviour checks | A |
| Contracts | Pydantic v2 | the shared data shapes between the lanes | A, all approve |
| Getting the acts | `httpx`, SPARQL | asks the EU's catalogue which acts exist, then downloads them | B |
| Reading the acts | `lxml` | cuts the text into sections and reads the duty table | A |
| Language model | PydanticAI | calls the model and forces typed, checkable answers | A |
| Model provider | one provider, picked on Tue 24 Nov after measuring 3 acts | long acts need a model that can read long texts; cost and limits decide | A |
| Model cache | a table in Postgres | the same question is never paid for twice | A |
| Traces and cost | Langfuse Cloud | shows every model call with tokens, cost and time | A |
| Name matching | scikit-learn, `rapidfuzz` | a small trained model on top of spelling scores | B |
| Experiment tracking | MLflow, local files | remembers every training run and its numbers | B |
| Database | Postgres | acts, ledger, Bergmann's lines, decisions, cache | B |
| Scheduling | CLI commands, GitHub Actions | the daily run, with no extra server | B |
| API | FastAPI, `uvicorn` | serves the data and the screens | C |
| Screens | the prototype's HTML and JS | the design is already tested; React only if its cost is named | C |
| Containers | Docker, Docker Compose | one command starts everything | A |
| Automatic checks | GitHub Actions | every pull request is checked the same way | A |
| Online hosting | Render | one web service and one database | A |

## Tools from the course we left out, and why

| Tool | Decision | Reason |
|---|---|---|
| dbt | Could | SQL views plus tests give the same checked ledger with one tool fewer |
| Prefect | Could | three commands and a scheduled job cover our runs |
| DVC | Could | about 200 compressed acts fit in git |
| Redis | not used | the cache is a database table |
| Prometheus, Grafana, Evidently | Could | traces and one cost report are enough at about two acts a week |
| LangChain, LangGraph | not used | PydanticAI covers typed extraction and tools |
| Qdrant and RAG | Could | finding an older measure is a database lookup, not retrieval |
| Kubernetes | Could | Docker Compose plus Render is what every lane can run |
| Fine-tuning | not used | too few labelled acts for four weeks |

A left-out tool may come back only if it replaces something. Never on top.

## Setup, once the code exists

1. `uv sync`, then `docker compose up -d postgres`.
2. Copy `.env.example` to `.env` and add your own model key. Never commit `.env`.
3. `uv run pytest`, `uv run ruff check`, `uv run ty check`.
4. `uv run tdd backfill --months 1` for a small first run, then `docker compose up`.

Run heavy jobs on a small sample first, one at a time. A heavy job can freeze a laptop.

## Model budget

- An act is 5,000 to 40,000 input tokens `[EST]`. The big example act, 2026/2393, is
  232 KB with 196 tables `[MEASURED 2026-11-13]`.
- Development costs far more than the exam: 40 practice acts times about 10 prompt
  versions is several million tokens `[EST]`.
- Free tiers often limit tokens per minute `[VERIFY]`. If they cannot carry development,
  the team agrees on a small shared budget with a hard cap.

## What you may honestly put on a CV at the end

| Claim | Only if |
|---|---|
| Structured extraction with a language model, with verification | the quote gate and the parser comparison run in the automatic checks |
| Evaluation on a sealed test set with intervals | the promise was committed before the single run |
| Entity matching model that beats a spelling baseline | both are reported on pairs labelled by someone else |
| Model judge with "not sure" and guardrails | the scope judge has its own test set and the number guard passes |
| Data pipeline, ledger with validity dates, scheduled job | the daily job works on the online desk |
| FastAPI, Docker, CI/CD, Render, Langfuse | the online desk works on presentation day |

Never claim: RAG, LangGraph, dbt, Prefect, DVC, fine-tuning or Kubernetes, unless the
matching Could item really shipped. Never claim "checked against TARIC".
