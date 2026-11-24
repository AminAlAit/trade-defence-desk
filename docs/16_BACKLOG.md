# 16 Backlog

All 73 work items. Each one is a GitHub issue with the same id in its title.
The issues are where the work happens. This page is the overview.

- **Size:** S is about half a day, M is one to two days, L is three days or more.
- **Priority:** Must, Should, Could. See [03_SCOPE.md](03_SCOPE.md).
- **Due:** the milestone. See [09_ROADMAP.md](09_ROADMAP.md).
- **Ids:** A, B and C are the lanes, X is shared work, K is extras. Some numbers are missing
  (A-12, B-14, B-16, B-17) because items were merged while planning.
- Inside each section, the items are in the order of their ids, not in the order of work.
  For the order of work, sort the issues by milestone.

## How much work is it?

Counting S as 0.5, M as 1.5 and L as 3 person-days `[EST]`:

| | Must items | Person-days |
|---|---|---|
| Shared work | 18 | 16.5 |
| Lane A: extraction and platform | 10 | 13 |
| Lane B: data and matching | 12 | 11.5 |
| Lane C: product and decisions | 13 | 11.5 |
| **Total** | **53** | **52.5** |

We have about 42 to 48 person-days `[EST]`. So the plan is tight on purpose, and
[09_ROADMAP.md](09_ROADMAP.md) says what shrinks first.

The three model pieces are never cut: A-03 with A-06, B-10 with B-11, C-07 with C-08.

## Shared work

| ID | Title | Priority | Size | Due | Done when |
|---|---|---|---|---|---|
| [X-01](https://github.com/AminAlAit/trade-defence-desk/issues/1) | Kickoff: lanes, working agreement, issues | Must | S | Mon 23 Nov | Lane owners are confirmed, the working agreement is accepted, and every Must item is an issue. |
| [X-02](https://github.com/AminAlAit/trade-defence-desk/issues/2) | Repository from the course template pattern (led by lane A) | Must | S | M1 | The folders `src/`, `tests/`, `data/evaluation/` and `reports/` exist; uv, ruff, ty and pytest run in the automatic checks; `main` is protected, or the checks act as the gate. |
| [X-03](https://github.com/AminAlAit/trade-defence-desk/issues/3) | Docker Compose with `api` and `postgres` (led by lane A) | Must | S | M1 | `docker compose up` works on at least two laptops by M1, and on the third by Tue 1 Dec. Extras sit behind a profile. |
| [X-04](https://github.com/AminAlAit/trade-defence-desk/issues/4) | Data shapes v1 (Pydantic contracts) and freeze (led by lane A, all approve) | Must | M | frozen Thu 26 Nov | All contracts listed in `docs/04_ARCHITECTURE.md` exist, with example files; frozen on Thu 26 Nov with approval from all three. |
| [X-05](https://github.com/AminAlAit/trade-defence-desk/issues/5) | Labelling guide and label file format (led by lane B, with lane A) | Must | S | M1 | The guide has an example for every hard case; `tdd labels check` validates label files. |
| [X-06](https://github.com/AminAlAit/trade-defence-desk/issues/6) | Recheck the domain facts against the current law (led by lane C, with lane A) | Must | S | M1 | Each fact in `docs/01_PRODUCT.md` is confirmed with article and paragraph, corrected, or removed from the screens. |
| [X-07](https://github.com/AminAlAit/trade-defence-desk/issues/7) | At least one conversation with a customs or trade person (led by lane C, with lane A) | Must | S | M2 | Notes on the three product bets in `docs/01_PRODUCT.md` are written down. |
| [X-08](https://github.com/AminAlAit/trade-defence-desk/issues/8) | Practice set: 40 acts, 10 of them labelled twice | Must | M | Wed 2 Dec | 40 valid label files by Wed 2 Dec; agreement on the double-labelled acts is reported as counts per field. |
| [X-09](https://github.com/AminAlAit/trade-defence-desk/issues/9) | Sealed exam: draw 25 acts by case and type, seal, label blind (led by lane B (keeper), with lane C) | Must | M | drawn Fri 27 Nov, labelled by Mon 7 Dec | Drawn and sealed on Fri 27 Nov; at least 12 acts with a company table; labelled by Mon 7 Dec; the owner of lane A never opens it. |
| [X-10](https://github.com/AminAlAit/trade-defence-desk/issues/10) | The written promise (pre-registration), in two steps (led by lane A) | Must | S | Fri 4 Dec and Thu 10 Dec | Numbers, bars and scoring code committed on Fri 4 Dec; model and prompt versions added and `holdout-freeze` tagged on Thu 10 Dec. |
| [X-11](https://github.com/AminAlAit/trade-defence-desk/issues/11) | Evaluation report, failure analyses and cards (led by lane A (editor), all) | Must | L | M4 | Everything is in `reports/`; every failure shows input, output, truth and cause. |
| [X-12](https://github.com/AminAlAit/trade-defence-desk/issues/12) | README with the results table (led by lane A) | Must | S | M4 | The README opens with the results table from `docs/10_EVALUATION.md`; setup takes four commands. |
| [X-13](https://github.com/AminAlAit/trade-defence-desk/issues/13) | Demo script, three rehearsals, a backup video (led by lane C (owner), all) | Must | M | M4 | The script is timed; at least three rehearsals are done; the video is saved with the release. |
| [X-14](https://github.com/AminAlAit/trade-defence-desk/issues/14) | Final slides | Must | M | M4 | Each lane has its own slides with its own numbers. |
| [X-15](https://github.com/AminAlAit/trade-defence-desk/issues/15) | Name test pairs: about 300, with look-alikes (led by lane B builds, lanes A and C label) | Must | S | labelled by Tue 1 Dec | A pairs file with its source acts; labels from lanes A and C only, done by Tue 1 Dec. |
| [X-16](https://github.com/AminAlAit/trade-defence-desk/issues/16) | Scope test pairs: about 120 (led by lane C builds, lanes A and B label) | Must | S | labelled by Tue 1 Dec | A pairs file; labelled by Tue 1 Dec; counts per class reported. |
| [X-17](https://github.com/AminAlAit/trade-defence-desk/issues/17) | Example files for acts 2026/2393 and 2026/2311 (led by lane A) | Must | S | day 3 | The tests of every lane can use them on day 3. |
| [X-18](https://github.com/AminAlAit/trade-defence-desk/issues/18) | Labelling viewer (led by lane C) | Must | S | M1 | It is used for the practice set and the sealed exam. |

## Lane A: extraction and platform

| ID | Title | Priority | Size | Due | Done when |
|---|---|---|---|---|---|
| [A-01](https://github.com/AminAlAit/trade-defence-desk/issues/19) | Text normaliser: sections, paragraph ids, spaces and decimal commas | Must | M | M1 | Acts 2026/2393 and 2026/2311 are split into title, recitals, articles and annexes, with stable ids. |
| [A-02](https://github.com/AminAlAit/trade-defence-desk/issues/20) | Duty-table parser with the grouped-cell logic | Must | L | M1 for one act, Tue 1 Dec for all practice layouts | The table of 2026/2393 gives the right rate and code per company, pinned by a test; all table layouts in the practice set pass by Tue 1 Dec. |
| [A-03](https://github.com/AminAlAit/trade-defence-desk/issues/21) | Model extraction agent (PydanticAI) | Must | L | M2 | It runs on the 40 practice acts with `openai/gpt-oss-120b` on Groq (reasoning effort low, temperature 0), typed output, a quote per field, company rows as a cross-check, tools and a call budget; tokens, cost and time are stored per act. |
| [A-04](https://github.com/AminAlAit/trade-defence-desk/issues/22) | Verifier: quote gate, value-in-quote, code check, consistency | Must | M | M2 | Every field has a status; a value must appear inside its own quote after cleaning; parser and model are compared; mismatches go to a person. |
| [A-05](https://github.com/AminAlAit/trade-defence-desk/issues/23) | Combined system and its rules | Must | S | M2 | Parser rows are cross-checked by the model; disagreements go to a person; coverage is logged. |
| [A-06](https://github.com/AminAlAit/trade-defence-desk/issues/24) | Evaluation harness | Must | M | M2 | One command produces the results table with intervals, the paired comparison and coverage; it refuses the sealed exam without the tag and writes a run id only once; a dry run works on the practice set; a 5-act subset runs in the automatic checks from recorded responses. |
| [A-07](https://github.com/AminAlAit/trade-defence-desk/issues/25) | Planted-error test | Must | S | M3 | The 20 plants are written by the owners of lanes B and C without reading the verifier code; the share caught is reported. |
| [A-08](https://github.com/AminAlAit/trade-defence-desk/issues/26) | Traces, cost and speed (Langfuse) | Must | S | M2 | One trace per act; cost per act and the slow end of the timing come from one query. |
| [A-09](https://github.com/AminAlAit/trade-defence-desk/issues/27) | Automatic checks on every pull request | Must | S | M1 | Lint, types, tests, engine checks and a cached evaluation subset are required for merging to `main`; the exam answers never enter the checks or their secrets. |
| [A-10](https://github.com/AminAlAit/trade-defence-desk/issues/28) | Online deploy on Render, with a check after each deploy | Must | S | M3 | The online desk passes `/health`, `/acts` and one case page after every deploy. |
| [A-11](https://github.com/AminAlAit/trade-defence-desk/issues/29) | Model reads what an amendment changes | Could | M | after M3 | The change is extracted, or the act goes to a person. |
| [A-13](https://github.com/AminAlAit/trade-defence-desk/issues/30) | Experiment: operative part against the whole act | Should | S | M3 | Tokens, cost and accuracy for both, on the practice set, in the report. |

## Lane B: data and matching

| ID | Title | Priority | Size | Due | Done when |
|---|---|---|---|---|---|
| [B-01](https://github.com/AminAlAit/trade-defence-desk/issues/31) | Queries that find the acts and notices | Must | S | M1 | The 30-day query returns the measured counts, or the difference is explained. |
| [B-02](https://github.com/AminAlAit/trade-defence-desk/issues/32) | Download and store the raw acts | Must | S | M1 | Each act is stored with fingerprint, size and time; the same act fetched twice is stored once. |
| [B-03](https://github.com/AminAlAit/trade-defence-desk/issues/33) | 24-month backfill, and counts per act type | Must | S | counts on Tue 24 Nov | About 200 acts are stored and committed compressed; the counts per type are reported and decide the make-up of the practice set and the exam. |
| [B-04](https://github.com/AminAlAit/trade-defence-desk/issues/34) | Commands and the daily job | Must | S | from week 3 | `tdd backfill`, `tdd daily` and `tdd replay` exist; the daily job runs as a scheduled GitHub Actions job against the online database. |
| [B-05](https://github.com/AminAlAit/trade-defence-desk/issues/35) | Triage: the act type from title rules | Must | S | frozen Fri 27 Nov | Every downloaded act has a type and a confidence; registration and initiation regulations still go to full extraction; the rules are frozen before the exam is drawn. |
| [B-06](https://github.com/AminAlAit/trade-defence-desk/issues/36) | Ledger: measures, rates, products, dates | Must | M | M2 | Tests on the validity dates pass; a measure shows its history. |
| [B-07](https://github.com/AminAlAit/trade-defence-desk/issues/37) | The states of a measure over time | Must | M | M2 | Each state has a test with a real act; amendments, corrections, suspensions and undertakings mark the measure for a person; no end date is computed. |
| [B-08](https://github.com/AminAlAit/trade-defence-desk/issues/38) | Product code list | Must | S | M1 | The source and the year are recorded; the verifier and the matching use the list. |
| [B-09](https://github.com/AminAlAit/trade-defence-desk/issues/39) | Synthetic importer generator | Must | M | M2 | 20 to 40 lines per importer with producer, product code, customs value, quantity, country of dispatch and invoice declaration; about a third fall under real acts; traders and decoys are included. |
| [B-10](https://github.com/AminAlAit/trade-defence-desk/issues/40) | Name matcher: baseline and trained model | Must | L | M2 | Four tiers and a safe threshold set on a validation split; training pairs are read as a stream; every run, with its Optuna settings, is logged in MLflow. |
| [B-11](https://github.com/AminAlAit/trade-defence-desk/issues/41) | Name matcher evaluation | Must | S | M3 | Baseline against trained model on the test pairs: how often it is right when it decides alone (with interval), the share sent to a person, and the share of true matches found. |
| [B-12](https://github.com/AminAlAit/trade-defence-desk/issues/42) | Dashboards and a drift report | Could | M | after M3 | A dashboard and one drift report. |
| [B-13](https://github.com/AminAlAit/trade-defence-desk/issues/43) | Link notices to measures | Must | S | M2 | Notices are linked by product and country; a notice that opens an expiry review shows on the case page of its measure and changes its status. |
| [B-15](https://github.com/AminAlAit/trade-defence-desk/issues/44) | Experiment: three ways to find the act type | Should | S | M3 | One quality score for all three; the trained model learns from the practice set only; the exam act types are labelled by the owner of lane C. |
| [B-18](https://github.com/AminAlAit/trade-defence-desk/issues/45) | Notices as early warnings in the inbox | Could | M | after M3 | A notice on a product in the importer's lines appears in the inbox. |

## Lane C: product and decisions

| ID | Title | Priority | Size | Due | Done when |
|---|---|---|---|---|---|
| [C-01](https://github.com/AminAlAit/trade-defence-desk/issues/46) | Screens: inbox, case page, decisions, proof | Must | M | M1 for the case page on example files, M2 for all screens | Inbox, case page, decisions and proof work in light and dark and at phone width. |
| [C-02](https://github.com/AminAlAit/trade-defence-desk/issues/47) | API endpoints | Must | M | M1, then with each feature | The paths for the M1 features exist, typed and tested; later paths arrive with their features. |
| [C-03](https://github.com/AminAlAit/trade-defence-desk/issues/48) | Euro engine, ported from the prototype | Must | M | M1 for the port, M2 for the rules | All 13 numbers of the prototype are reproduced; tests cover two duties on one line, the provisional collection rule and registration only. |
| [C-04](https://github.com/AminAlAit/trade-defence-desk/issues/49) | Match purchase lines by product code and origin | Must | S | M1 | A 10-digit code decides when the line has one; an "ex" code without it is unsure; an extended measure sends the line to a person. |
| [C-05](https://github.com/AminAlAit/trade-defence-desk/issues/50) | Decisions list and audit log | Must | M | M2 | Every decision is a log entry; a reason is required for "continue unverified"; the export includes the log. |
| [C-06](https://github.com/AminAlAit/trade-defence-desk/issues/51) | Highlighted quotes | Must | S | M2 | Clicking a field highlights its sentence; a quote that is not found word for word shows amber. |
| [C-07](https://github.com/AminAlAit/trade-defence-desk/issues/52) | Scope judge | Must | M | first version on 3 acts by M2, full by M3 | It runs on every possibly covered line of acts with scope limits or exclusions. |
| [C-08](https://github.com/AminAlAit/trade-defence-desk/issues/53) | Scope judge evaluation | Must | S | M3 | Right answers, missed cases and "not sure" answers as counts with an interval; once with the correct exclusions given, once end to end. |
| [C-09](https://github.com/AminAlAit/trade-defence-desk/issues/54) | Plain-language summary of each act | Could | M | after M3 | It passes the number guard. |
| [C-10](https://github.com/AminAlAit/trade-defence-desk/issues/55) | Replay | Must | S | M2 | Twelve months of runs play back at a pace we set for the presentation, marked "replay". |
| [C-11](https://github.com/AminAlAit/trade-defence-desk/issues/56) | Checklist and drafts from templates | Should | S | M3 | Numbers appear only through template fields. |
| [C-12](https://github.com/AminAlAit/trade-defence-desk/issues/57) | Proof export | Must | S | M3 | One Markdown file per case with version, quotes, decisions, assumptions and "not checked" lines. |
| [C-13](https://github.com/AminAlAit/trade-defence-desk/issues/58) | CSV upload with a check per row | Must | S | M2 | Wrong rows are listed with a reason. |
| [C-14](https://github.com/AminAlAit/trade-defence-desk/issues/59) | Email digest | Could | S | after M3 | One digest a day for new hits. |
| [C-15](https://github.com/AminAlAit/trade-defence-desk/issues/60) | Usability test with two cohort members | Must | S | M4 | Notes and fixes are in `reports/`. |
| [C-16](https://github.com/AminAlAit/trade-defence-desk/issues/61) | Experiment: two models on the scope judge | Should | S | M3 | Right answers, "not sure" rate and cost for both. |
| [C-17](https://github.com/AminAlAit/trade-defence-desk/issues/62) | Number guard | Must | S | M3 | An automatic test fails on any digit the model wrote outside a word-for-word quote. |

## Extras (Could), only after M3, one owner each

| ID | Title | Priority | Size | Due | Done when |
|---|---|---|---|---|---|
| [K-01](https://github.com/AminAlAit/trade-defence-desk/issues/63) | UK as a second authority | Could | M | after M3 | Twenty labelled acts, with the interval shown. |
| [K-02](https://github.com/AminAlAit/trade-defence-desk/issues/64) | US anti-dumping notices | Could | M | after M3 | The different way the US collects duties is modelled and marked as unverified until checked. |
| [K-03](https://github.com/AminAlAit/trade-defence-desk/issues/65) | German templates and German act text | Could | M | after M3 | The German text route is tested first. |
| [K-04](https://github.com/AminAlAit/trade-defence-desk/issues/66) | WhatsApp window | Could | M | after M3 | Works for one supplier question end to end. |
| [K-05](https://github.com/AminAlAit/trade-defence-desk/issues/67) | Similar labelled acts as examples for the model | Could | M | after M3 | Examples come from the practice set only, never from the sealed exam. |
| [K-06](https://github.com/AminAlAit/trade-defence-desk/issues/68) | Study across authorities | Could | M | after M3 | Promised in writing first; a "no" is a fine result. |
| [K-07](https://github.com/AminAlAit/trade-defence-desk/issues/69) | Supplier press check | Could | M | after M3 | Only started if at least 5 of the 14 newest acts have news on an exporter. |
| [K-08](https://github.com/AminAlAit/trade-defence-desk/issues/70) | Value ledger: hours saved | Could | M | after M3 | Machine times are measured; human times stay marked as assumptions. |
| [K-09](https://github.com/AminAlAit/trade-defence-desk/issues/71) | Kubernetes | Could | M | after M3 | Only if the release check runs on it. |
| [K-10](https://github.com/AminAlAit/trade-defence-desk/issues/72) | dbt, Prefect, DVC | Could | M | after M3 | Add one only if it replaces something, never on top. |
| [K-11](https://github.com/AminAlAit/trade-defence-desk/issues/73) | Live run view | Could | M | after M3 | The stored replay already covers the presentation; this is the live version. |
