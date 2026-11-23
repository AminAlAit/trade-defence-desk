# 03 Scope: what we build in four weeks, and what we do not

## The three priority words

| Word | Meaning |
|---|---|
| **Must** | The capstone fails without it. |
| **Should** | Planned, but the first thing we drop if we are behind. |
| **Could** | Extra. Only after the Friday 11 Dec milestone is reached, with one owner each. |
| **Won't** | Not in this capstone. We say so openly. |

## The one rule

**Real acts, one synthetic importer, EU only.** Should items wait until the second
Friday (M2, 4 Dec) is reached. Could items wait until the third Friday (M3, 11 Dec).

The Must list is about 52.5 person-days. We have about 42 to 48 `[EST]`. So the plan is
tight on purpose, and the order in which we shrink is already written down
(see [09_ROADMAP.md](09_ROADMAP.md)).

## Must

| Area | What | Issues |
|---|---|---|
| Team setup | repo, one command to start, automatic checks, shared data shapes, example files, labelling guide and viewer | X-01 to X-05, X-17, X-18, A-09 |
| Getting the acts | find and download the acts of the last 24 months; store them unchanged; then a daily run | B-01 to B-04 |
| Triage | the type of each act, from rules on its title | B-05 |
| Extraction | Python reads the duty tables; the model reads scope, dates and "which older act does this change", with a quote per field | A-01 to A-03, A-05 |
| Checking | the quote gate, product code check, consistency, parser against model; every field gets a status | A-04, A-07 |
| Ledger | one card per measure with its rates, dates and state | B-06, B-07, B-08, B-13 |
| Importer | the synthetic importer, uploaded as CSV and checked | B-09, C-13 |
| Matching | product code and origin; producer names with a baseline and a trained model; unsure cases go to a person | C-04, B-10 |
| Scope judge | is this line outside the act's scope? quote or "not sure"; a person confirms | C-07, C-17 |
| Money | the euro engine, ported from the prototype, with its 13 checks as tests | C-03 |
| Decisions and proof | one decisions list, a log with reasons, highlighted quotes, an export | C-05, C-06, C-12 |
| Screens | inbox, case page, decisions, proof, and the replay | C-01, C-02, C-10 |
| Evaluation | practice set, sealed exam, test pairs, the written promise, one exam run | X-08 to X-10, X-15, X-16, A-06, B-11, C-08 |
| Operations | traces and a cost report; the online deploy with a check after each deploy | A-08, A-10 |
| Reality checks | domain facts rechecked; one talk with a customs person; a usability test | X-06, X-07, C-15 |
| Write-up | results table, report, failure analyses, slides and demo | X-11 to X-14 |

## Should

| What | Issue |
|---|---|
| Does the model do better with the whole act or only the operative part? | A-13 |
| Title rules against a small trained model against a language model, on the act type | B-15 |
| Two models compared on the scope judge | C-16 |
| Checklist and drafts from templates | C-11 |

## Could

More countries (UK, US), German texts, early warnings from notices, an email digest, a
WhatsApp window, a plain-language summary per act, dashboards, and the course tools we left
out. The full list is in [16_BACKLOG.md](16_BACKLOG.md), section K.

## Won't

- Checking against TARIC. No free structured feed exists `[MEASURED 2026-11-13]`.
- Deciding the origin of goods, or giving legal advice.
- Safeguards: shown, not applied.
- Applying amendments, corrections, suspensions, undertakings and rates that are not a
  simple percentage. They are shown with the act's quote and sent to a person.
- Real customer data.
- Forecasting rates or outcomes.
- Fine-tuning a model.
- User accounts beyond a simple demo login.

## When are we done?

1. `docker compose up` gives a working desk on a fresh laptop in under 15 minutes.
2. The online desk shows Bergmann's inbox with real acts, and the daily job adds new ones.
3. The README opens with the results table from the sealed exam.
4. Every number on screen links to the sentence or the assumption it came from.
5. Every pull request is checked automatically.
6. Each lane has a failure analysis with real cases.
7. The presentation has been rehearsed three times, and a backup video exists.

## The scope guard

When someone proposes something new, ask three questions:

1. Is it in "Must"?
2. If not: is M2 reached (for a Should item), or M3 (for anything else)?
3. Who owns it, and what do they drop for it?

If any answer is "no" or "nobody", the idea goes into the "Later" list in
[11_DECISIONS.md](11_DECISIONS.md).
