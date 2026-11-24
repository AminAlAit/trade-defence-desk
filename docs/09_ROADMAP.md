# 09 Roadmap

Mon 23 Nov to Fri 18 Dec 2026. The final presentation is on 17 or 18 Dec `[VERIFY]`.
Course days still take time, so we count on 14 to 16 real working days per person `[EST]`.

## Four Fridays

| | Date | Name | It is reached when |
|---|---|---|---|
| **M1** | Fri 27 Nov | Walking skeleton | One real act (2026/2393) goes through the pipeline: downloaded, cut into sections, duty table parsed, stored, shown on a case page. Automatic checks are green. `docker compose up` works on two laptops. Data shapes frozen Thu 26 Nov. Sealed exam drawn and sealed. |
| **M2** | Fri 4 Dec | A real desk on real acts | Practice acts read by parser, model and verifier. Ledger with dates. Bergmann matched. Euros, decisions and highlighted quotes on screen. The replay plays. Practice set complete. First numbers for all three model pieces. First half of the written promise committed. |
| **M3** | Fri 11 Dec | Feature freeze and the exam | Online on Render. Daily job runs. `holdout-freeze` tagged Thu 10 Dec. The exam runs once on Fri 11 Dec. Results table filled. |
| **M4** | Thu 17 or Fri 18 Dec | Final presentation | README, report, failure analyses merged. Three rehearsals. Backup video recorded. |

## Before anyone builds: six checks

1. Ask the coaches the five questions in [11_DECISIONS.md](11_DECISIONS.md).
2. Check whether GitHub can protect the `main` branch on our plan. If not, the automatic
   checks are the gate and the rule holds by agreement.
3. Check the free-tier limits of Render `[VERIFY]`: does the database expire, does the
   service sleep?
4. Use Langfuse Cloud, not a self-hosted Langfuse `[VERIFY limits]`.
5. Everyone checks that Docker Desktop and `uv` run on their laptop.
6. Confirm the reuse terms of the act texts. Keep the name-pair training data out of this
   repository.

## Week 1: Mon 23 to Fri 27 Nov

| Day | Lane A | Lane B | Lane C | Together |
|---|---|---|---|---|
| Mon 23 | repo and automatic checks; first draft of the data shapes; example files started | the queries that find acts and notices | prototype served by FastAPI, case page on the example file; read the current basic regulation | kickoff |
| Tue 24 | **measure 3 acts** with each candidate model provider (done: see `07_TECH_STACK.md`); start cutting text into sections | download 24 months of acts, raw only; report how many of each type | first API endpoints; start porting the euro engine | choose the model provider and the budget; write to 2 or 3 customs contacts |
| Wed 25 | sections done; parser starts; Docker Compose | source for the product code list | euro engine and its 13 checks; labelling viewer | labelling guide; 1 hour of practice labelling each |
| Thu 26 | parser on 2026/2393 with the grouped-cell test | title rules for triage | product code and origin matching | **freeze the data shapes**, approved by all three |
| Fri 27 | parser output into the database, shown on the case page | **freeze the title rules, draw and seal the exam** | case page reads from the API | **M1 demo and retro**; 2 hours of practice labelling each |

Two rules for week 1:

- Until the exam is drawn on Friday, nobody runs extraction on the downloaded acts. Only
  downloading and title rules run.
- The two example acts, 2026/2393 and 2026/2311, always belong to the practice set.

## Week 2: Mon 30 Nov to Fri 4 Dec

| Lane | Work |
|---|---|
| A | parser passes all table layouts in the practice set by Tue 1 Dec; model extraction with quotes; verifier; combined system; evaluation harness on the practice set; traces and cost report |
| B | ledger with dates; the states of a measure; notice links; synthetic importer; name test pairs mined; name matcher baseline and first trained model |
| C | decisions list and log; highlighted quotes; CSV upload; replay; scope test pairs built; first scope judge on 3 acts |
| Together | name and scope pairs labelled by **Tue 1 Dec**; practice set finished by **Wed 2 Dec**; Wednesday pair sessions; planted errors written; first half of the written promise on **Fri 4 Dec**; **M2 demo** |

### If we are behind on Fri 4 Dec

Drop the Should items first: A-13, B-15, C-16, C-11. Then shrink these Must items, in
this order:

1. C-12 proof export: down to a copy of the log as text.
2. C-05 log: down to decisions with reasons, without filters.
3. B-07 states: down to registration, provisional to definitive, and repeal. Everything
   else goes to a person. Never down to a computed end date.
4. C-01 screens: down to three: inbox, case page, decisions.
5. A-05 combined system: down to parser plus verifier.

**Never cut:** the three model pieces with their evaluations (A-03 with A-06, B-10 with
B-11, C-07 with C-08). They may shrink. Each keeps its test set and its line in the README.

## Week 3: Mon 7 to Fri 11 Dec

| Lane | Work |
|---|---|
| A | online deploy with a check after each deploy; planted-error test; the A-13 experiment if M2 was reached; **dry run of the exact exam command on the practice set, then tag `holdout-freeze` on Thu 10 Dec**; run the exam once on **Fri 11 Dec** |
| B | daily job against the online database; name matcher evaluation; triage study if time; exam labels done by **Mon 7 Dec** |
| C | scope judge with "not sure", and its evaluation; number guard; proof export; model comparison if time; usability test booked |
| Together | **feature freeze Thu 10 Dec**: after it only fixes, tests and docs. Friday **M3**: results table filled, first full run-through of the demo |

## Week 4: Mon 14 to Fri 18 Dec

| Day | Work |
|---|---|
| Mon 14 | each lane writes its failure analysis; usability test; rehearsal 1, timed |
| Tue 15 | report merged; README with the results table; "who did what" page |
| Wed 16 | slides final; rehearsal 2; record the backup video |
| Thu 17 | rehearsal 3 in the morning, or the presentation itself |
| Fri 18 | the presentation if it is on the 18th; tag `v1.0` |

## The weekly rhythm

| When | What | How long |
|---|---|---|
| every working day | standup: done, today, blocked? | 15 min |
| Wednesday | pair sessions (week 2), or a review of open pull requests | 60 to 90 min |
| Friday | milestone demo, each lane shows its numbers; then a retro: keep, change, try | 45 min |

## Warning signs to check every Friday

- M1 slips past Mon 30 Nov.
- Fewer than 30 practice acts labelled on Mon 30 Nov, or the test pairs not labelled on Tue 1 Dec.
- A lane has no model number on Fri 4 Dec.
- The automatic checks on `main` are red for more than a day.
- A pull request has waited more than two days for review.
