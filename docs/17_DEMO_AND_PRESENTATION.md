# 17 Demo and final presentation

The plan for the last day. Length and format are `[VERIFY]` with the coaches. This plan
assumes 12 minutes plus questions.

## The story in one breath

"The EU keeps putting extra duties on products from specific producers abroad. An importer
finds out late, and then searches a long act by hand for its supplier's name. Our desk
reads every act on the day it is published, checks every fact against the text, finds your
producers, and shows what is at stake, without the model ever writing a number."

## We play it as a game

The audience follows Bergmann Outdoor through one year. Twelve months of real acts are
replayed, sped up, at a pace we set, and marked "replay" on screen. Then the newest real
act runs live.

## Running order

Each person presents their own lane.

| Part | Lane | On screen | The point |
|---|---|---|---|
| 1 | A | Thomas's Monday: an act came out on Friday, two shipments are at sea | the problem in human terms; rates are per producer |
| 2 | B | the replay of Bergmann's year: the ledger fills, a definitive act settles what a provisional one secured, a review notice keeps a measure alive, a repeal ends another | it runs on its own, on real data; it is a ledger, not a list |
| 3 | C | the newest act, live; the case page and its six questions; one amber field; the name decision that turns a range into one figure; the proof export | a person decides, the money moves, every number has a sentence |
| 4 | A | the results table from the sealed exam: three systems, intervals, coverage, n; one real failure; the planted errors | why you can trust it, and where you should not |
| 5 | B | the name matcher against its baseline; one hard pair | a model where it belongs, with its own honest test |
| 6 | C | the scope judge: right, missed, "not sure"; the number guard at zero; one finding from the usability test | model features with guardrails |
| 7 | all | one trace with cost and time; people decide what the program cannot prove; the limits | engineering maturity and honesty |

For part 3, use a case where the named rate differs from the fallback rate. Hubei Unibon
(39,8 %) against all other imports (48,1 %) works. The two Tiandingfeng names do not:
their 48,1 % equals the fallback, so nothing would move on screen.

## What must never happen on stage

- Saying "checked against TARIC", "exempt", "will cost" or "final".
- Showing a score that is not ours.
- A number written by the model on a slide or a screen.
- Calling the replay "live".

## Rehearsals

| When | What |
|---|---|
| Fri 11 Dec | first full run-through, untimed; list what breaks |
| Mon 14 Dec | rehearsal 1, timed, with someone outside the team watching |
| Wed 16 Dec | rehearsal 2; record the backup video |
| presentation day, morning | rehearsal 3; wake the online desk; start the laptop version as a spare |

## If something breaks live

1. the online desk;
2. the desk on a laptop;
3. the backup video, with the presenter talking over it;
4. screenshots in the slides.

## Questions to expect

| Question | Who answers |
|---|---|
| "Your parser and the model disagree on a rate. Which one wins?" | lane A: neither; a person looks. Show a real case. |
| "How do you know you did not tune on the test set?" | lane A, then the exam keeper |
| "What happens when an act changes an older act?" | lane B |
| "Why not just use TARIC?" | lane C |
| "What does it cost per act, and how fast is it?" | lane A |
| "Would a real customs department use this?" | lane C, with the notes from the customs conversation |
| "Why no RAG, no LangGraph?" | lane A: finding an older measure is a database lookup; we use an agent with typed tools |
