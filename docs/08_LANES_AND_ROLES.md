# 08 Lanes, roles and responsibilities

## The idea behind the split

All three of us want hands-on work with language models and machine learning. So the split
follows one rule:

> **Every lane owns one real model piece that is a Must.** Each piece has its own test set,
> labelled by someone else, and its own line in the results table.

Each lane also has one smaller experiment as a Should.

A lane has one owner. The owner is whoever took the lane at the kickoff. This page names
lanes, not people, so it stays true if we swap.

## Lane A: extraction and platform

**Mission:** turn an act into checked facts, and prove how often they are right.

Owns:

- the shared data shapes (the contracts) and the example files for two real acts;
- cutting the text into sections, and the duty-table parser;
- the extraction with the language model, and the verifier;
- the evaluation harness, the written promise before the exam, and the README;
- traces and the cost report;
- the repository, Docker Compose, the automatic checks and the online deploy.

| | |
|---|---|
| **Must model piece** | the extraction agent, and the comparison of three systems on the sealed exam |
| **Should experiment** | whole act against operative part only (A-13) |
| **The story to tell afterwards** | "Our parser and the model disagreed on a duty rate. Here is the grouped cell that caused it, and here is how the combined system scored on acts nobody had tuned on." |

## Lane B: data and matching

**Mission:** get every act in, keep the ledger true over time, and find the importer's
producers in the duty tables.

Owns:

- finding and downloading the acts, the 24-month backfill and the daily job;
- the triage rules, the list of product codes, and the ledger;
- the generator for the synthetic importer;
- the name matcher;
- the sealed exam: drawing it, sealing it, labelling it, settling disagreements;
- the labelling guide.

| | |
|---|---|
| **Must model piece** | the name matcher: a trained model against a spelling-score baseline |
| **Should experiment** | title rules against a small trained model against a language model, on the act type (B-15) |
| **The story to tell afterwards** | "The duty table said one spelling, the invoice said another. Here is what training added over a spelling score, how often the matcher may decide alone, and how much it hands to a person." |

## Lane C: product and decisions

**Mission:** make the desk usable by someone new to customs, make every number traceable,
and let a model help without letting it decide.

Owns:

- the screens, built from the prototype, and the API;
- matching by product code and origin;
- the euro engine;
- the decisions list, the log, highlighted quotes and the proof export;
- the replay;
- the labelling viewer;
- rechecking the domain facts, and the talk with a customs person;
- the demo, with everyone.

| | |
|---|---|
| **Must model piece** | the scope judge: is this purchase line outside the act's scope? Quote or "not sure"; a person confirms |
| **Should experiment** | two models on the same test pairs (C-16) |
| **The story to tell afterwards** | "The model may explain why a product is outside the scope, but it may not write a single number. Here is the guard that enforces it, and how often the judge said 'not sure' instead of guessing." |

## Shared work

Some work belongs to everyone: labelling the practice set, the test pairs, the report, the
slides and the rehearsals. In the issues it carries the label `lane: shared`.

## Shared roles

| Role | Who | What it means |
|---|---|---|
| Facilitator | rotates: one person per week, all three in week 4 | runs the daily standup and the Friday review, keeps the issues current |
| Contract keeper | owner of lane A | a change to a frozen data shape needs a pull request approved by all three |
| Exam keeper | owner of lane B | draws and seals the exam, plans who labels what |
| Exam co-labeller | owner of lane C | labels the exam together with the keeper |
| Labelling coordinator | owner of lane B | the guide and the schedule |
| Platform | owner of lane A | repo, Compose, checks, deploy; the exam answers never enter the automatic checks |
| Demo owner | owner of lane C | the script, the rehearsals, the backup video |
| Report editor | owner of lane A | merges three lane reports into one report and one README |
| Domain checker | owner of lane C, with lane A | checks the domain facts and the wording rules |

**One hard rule:** the owner of lane A never opens the sealed exam. Lane A builds the
thing the exam grades.

## Nobody grades their own homework

| Piece | Built by | Its test answers come from |
|---|---|---|
| Extraction (parser, model, verifier) | lane A | lanes B and C (the sealed exam) |
| Planted errors for the verifier | run by lane A | written by B and C, without reading the verifier |
| Name matcher | lane B | lanes A and C |
| Triage study | lane B | practice labels by all; exam act types by lane C |
| Scope judge | lane C | lanes A and B |

## Who answers for what

Four words: a lane **owns** a deliverable (it answers for it; one lane only), **does**
work on it, is **asked** before decisions, or is **told** afterwards.

| Deliverable | Lane A | Lane B | Lane C |
|---|---|---|---|
| Repo, Compose, automatic checks (X-02, X-03, A-09) | owns, does | asked | told |
| Data shapes, freeze, example files (X-04, X-17) | owns, does | asked | asked |
| Labelling guide (X-05) and viewer (X-18) | asked | owns, does (guide) | does (viewer) |
| Getting the acts, backfill, daily job (B-01 to B-04) | asked | owns, does | told |
| Triage rules and study (B-05, B-15) | asked | owns, does | asked |
| Sections, parser, model extraction, verifier (A-01 to A-05) | owns, does | asked | told |
| Planted errors (A-07) | owns (runs it) | does (writes them) | does (writes them) |
| Ledger, states, notice links (B-06, B-07, B-08, B-13) | asked | owns, does | told |
| Synthetic importer (B-09) | told | owns, does | asked |
| Name matcher and its test pairs (B-10, B-11, X-15) | does (labels) | owns, does | does (labels) |
| Product matching, euro engine (C-03, C-04) | asked | asked | owns, does |
| Decisions, log, quotes, export (C-05, C-06, C-12) | told | asked | owns, does |
| Scope judge, its pairs, number guard (C-07, C-08, X-16, C-17) | does (labels) | does (labels) | owns, does |
| Screens and replay (C-01, C-02, C-10) | told | told | owns, does |
| Practice set (X-08) | owns, does | does | does |
| Sealed exam (X-09) | told (never sees it) | owns, does | does |
| Written promise and exam run (X-10, A-06) | owns, does | asked | asked |
| Traces and cost report (A-08) | owns, does | told | told |
| Online deploy (A-10) | owns, does | asked | told |
| Domain facts, customs talk (X-06, X-07) | does | told | owns, does |
| Report and README (X-11, X-12) | owns, does | does (own lane) | does (own lane) |
| Demo, slides, rehearsals (X-13, X-14) | does | does | owns, does |

## How much work each lane carries

Counted in person-days for the Must items `[EST]`: shared 16.5, lane A 13, lane B 11.5,
lane C 11.5. Lane A carries the most, because the platform work sits there.

Labelling by hand is on top, and it is unequal on purpose: about 8 hours for the owner of
lane A, 15 for lane B and 14 for lane C. The owner of lane A never labels the exam.

## So everyone touches more than their lane

- **Weeks 1 and 2:** everyone labels practice acts. It is the fastest way to learn the domain.
- **Week 2, Wednesday:** three 90-minute pair sessions, each on someone else's model piece.
  The test pairs are labelled before these sessions, so seeing the code cannot bias the labels.
- **Week 3:** each person reviews at least two pull requests from each other lane.
- **Fridays:** each person shows their own lane's model result, with numbers.
- **Final presentation:** each person presents their own lane.
