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
| Language model | `openai/gpt-oss-120b` on Groq | reads the acts and judges the scope; see "The models, piece by piece" | A, C |
| Model cache | a table in Postgres | the same question is never paid for twice | A |
| Traces and cost | Langfuse Cloud | shows every model call with tokens, cost and time | A |
| Name matching | `rapidfuzz`, scikit-learn, Optuna | spelling scores, then a small trained model tuned with Optuna | B |
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

## The models, piece by piece

| Piece | Lane | Model | Compared with |
|---|---|---|---|
| Extraction agent (A-03) | A | `openai/gpt-oss-120b` on Groq, reasoning effort "low", temperature 0, through PydanticAI | the parser alone, and the model alone (the three systems in [10_EVALUATION.md](10_EVALUATION.md)) |
| Name matcher (B-10) | B | logistic regression, then a random forest; both scikit-learn, tuned with Optuna, logged in MLflow; the better one on the validation split is kept | a `rapidfuzz` spelling score with a threshold |
| Scope judge (C-07) | C | the same `openai/gpt-oss-120b` on Groq | always "inside the scope" |
| Act-type study (B-15, Should) | B | TF-IDF plus logistic regression (scikit-learn), and `openai/gpt-oss-120b` without examples | the title rules |
| Second model (C-16, Should) | C | `ministral-14b-latest` on Mistral | `openai/gpt-oss-120b` on the same test pairs |

One model for every reported number, so the numbers can be compared (D-24). The name
matcher's inputs are the signals listed in
[examples/04_WHOSE_NAME_IS_IT.md](examples/04_WHOSE_NAME_IS_IT.md).

### How the model was chosen

On Tue 24 Nov we sent the articles and annex of three real acts (2026/2393, 2026/1063,
2026/2311) to the models of the four providers we had keys for. Same prompt, temperature
0. We counted the company rows (8, 8 and 1) and checked every quote against the act
`[MEASURED 2026-11-24]`:

| Model | Rows right | Grouped cell right | Quotes found in the act | Seconds per act | Free-tier limit |
|---|---|---|---|---|---|
| `openai/gpt-oss-120b`, Groq | 17 of 17 | 2 of 2 | 19 of 20 | about 2 | 8,000 tokens a minute, about 1,000 requests a day |
| `ministral-14b-latest`, Mistral | 17 of 17 | 2 of 2 | 9 of 10 | about 4 | 2 requests a minute, 40,000 tokens a minute |
| `openai/gpt-oss-20b`, Groq | 17 of 17, plus 2 invented rows | 0 of 2 | 16 of 22 | about 1 | as for the 120b |
| `gemma-4-26b-a4b-it`, Google and OpenRouter | no answer | | | | timeouts and rate limits |

`openai/gpt-oss-20b` first returned nothing at all: with default settings it spent its whole
answer on reasoning. Setting the reasoning effort to "low" fixed that.

Three acts are a smoke test, not a result. All three belong to the practice set (the two
fixed example acts, and 2026/1063 because it is the same case as 2026/2393).

## Setup, once the code exists

1. `uv sync`, then `docker compose up -d postgres`.
2. Copy `.env.example` to `.env` and add your own model key. Never commit `.env`.
3. `uv run pytest`, `uv run ruff check`, `uv run ty check`.
4. `uv run tdd backfill --months 1` for a small first run, then `docker compose up`.

Run heavy jobs on a small sample first, one at a time. A heavy job can freeze a laptop.

## Model budget

- **The part we send is small.** The articles and annex of an act are about 300 to 1,050
  tokens. A whole act is 15,000 to 45,000 `[MEASURED 2026-11-24, counted as characters
  divided by 4]`. One call with its answer used about 1,500 to 2,200 tokens.
- **So the free tier carries development.** At about 2,000 tokens a call, Groq's free tier
  allows about 4 acts a minute and about 1,000 calls a day `[MEASURED 2026-11-24]`. 40
  practice acts times 10 prompt versions is 400 calls, spread over days.
- **The whole act does not fit.** A whole act is above Groq's free limit of 8,000 tokens a
  minute. The experiment in A-13 (whole act against the operative part) therefore needs
  a small paid budget, or must use the 40,000-token minute on Mistral for the shorter acts.
- **Each person uses their own free key** during development. The exam runs once on one
  team key (D-25).

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
