# 10 How we know it works

The evaluation is the real deliverable. A desk that looks good but is right only sometimes
is worth nothing to Thomas, and the course grades the evaluation report and our honesty
about failures.

## Two sets of acts

| Set | Size | Who writes the correct answers | Used for |
|---|---|---|---|
| **Practice set** | 40 acts | all three; 10 acts are labelled twice | building and tuning the parser, the prompts and the verifier |
| **Sealed exam** | 25 acts, at least 12 with a company table | the owners of lanes B and C only; 5 acts labelled twice | the one result we report |

"Labelling" means: a person reads the act and writes down the correct answers by hand, in
a YAML file. The labelling guide says how (issue X-05). A sample file is in
[examples/sample_label_32026R2393.yaml](examples/sample_label_32026R2393.yaml).

### How labelling works

- **Practice set:** you may start from the parser's output and correct it. About 12 to 15
  minutes per act `[EST]`.
- **Sealed exam:** from the act text only. No parser or model output in view. About 30 to
  40 minutes per act `[EST]`.
- A command, `tdd labels check`, tells you whether your file has the right shape.
- Every label file holds: the act type, the products and codes, every company row with
  its kind, the dates, and the fine print (the invoice declaration word for word, what
  happens to the provisional amounts, anything collected backwards, the new-exporter
  clause, the price base).
- The guide answers the hard questions with one example each: what counts as one row,
  what to do with a grouped cell, how to write an "ex" code, when an amendment changes a row.
- Where two people labelled the same act, we count per field how often they agree.
- In total about 35 to 45 hours of labelling for the team `[EST]`.

Smaller sets for the other two model pieces:

| Set | Size | Labelled by | Tests |
|---|---|---|---|
| Name test pairs | about 300 pairs of names | lanes A and C | the name matcher |
| Scope test pairs | about 120 pairs of (purchase line, act) | lanes A and B | the scope judge |

## The exam: five rules

1. **Split by case, not by act.** A provisional act and the definitive act of the same
   product share companies and wording. So whole cases go either to practice or to the exam.
2. **Drawn on Fri 27 Nov** by the exam keeper, with a fixed random seed, after the title
   rules are frozen.
3. **Hidden from the pipeline.** Only fingerprints of the exam act ids are in the
   repository. The pipeline skips those acts until the run. The answers live outside the
   repository.
4. **Opened by two people only.** The owner of lane A never sees the exam.
5. **Run once, enforced by code.** The exam command refuses to run without the
   `holdout-freeze` tag, and writes its run id to a file it never overwrites. A second run
   is allowed only after a technical failure, with the same setup, and is logged. An act
   that fails to parse counts as wrong, not as missing.

An honest limit: with three people, "blind" is relative. The two labellers also see lane
A's work in reviews and demos. The report says so.

## The main number

**Table accuracy:** an act counts as correct when every company row the system accepted on
its own equals the hand-written table. A row is name, rate and code together.

It is always reported next to **coverage**: the share of acts where the system sent
nothing to a person.

We compare three systems on the same acts:

| System | Rows come from | What it tests |
|---|---|---|
| Parser only | the parser, all accepted | the Python parser |
| Model only | the model's own reading, all accepted | the model on tables |
| Combined | parser rows, cross-checked by model and verifier; disagreements go to a person | the safety net |

- **The bar:** at least 90 % for the combined system.
- **The honest part:** with 25 acts, even a perfect score proves little. 25 of 25 correct
  gives a 95 % interval that starts at about 86 %. So we report the interval and do not
  claim more than it shows.
- **Say it plainly:** in the combined system the rows are the parser's. So the main number
  mostly tests the parser plus the decision "accept or send to a person". The model's own
  skill shows in the "model only" row and in the fields it reads alone.
- **Intervals:** the Wilson method; at exactly 0 % or 100 % the stricter exact method
  (Clopper-Pearson). Row-level numbers get a bootstrap that redraws whole acts.
- **Comparing systems:** all three run on the same acts. We report the acts on which they
  differ, and an exact McNemar test on those.
- We always state n, for example "n = 12 acts with a company table".

A worked example with numbers is in
[examples/09_GRADING_THE_DESK.md](examples/09_GRADING_THE_DESK.md).

## Other numbers, for information only

| What | How it is counted |
|---|---|
| company rows | share of rows found, and share of found rows that are right |
| the "all other imports" rate | right or wrong |
| product codes in scope | exact set per act |
| origin countries, dates, "which older act does this change" | exact match |
| quote gate | share of model fields whose quote is found and contains the value |
| planted errors | how many of 20 the verifier catches |
| model-written numbers outside quotes | must be 0; a hard rule, not a score |
| cost and speed | tokens, euros and seconds per act |

## The other two model pieces

| Piece | Main number | Compared with | The error that hurts most |
|---|---|---|---|
| Name matcher | how often it is right when it decides alone; how much it hands to a person | a plain spelling score with a threshold | a true match missed: the supplier silently gets the fallback rate |
| Scope judge | right answers, missed cases, "not sure" answers, as counts | "never outside the scope" | a covered line wrongly called outside: Thomas misses a duty |
| Triage study (Should) | quality across act types | the title rules | a duty act read as "other" |

## The written promise (pre-registration)

Before we see any exam result, we write down how we will score. That way nobody can pick
the flattering number afterwards.

1. **Fri 4 Dec:** commit the main number and its bar, the other numbers marked "for
   information", the interval method, the exact inputs per system and the scoring code.
2. **Thu 10 Dec:** add the model, provider and prompt versions. Run the exact exam command
   once on the practice set as a dry run. Tag the commit `holdout-freeze`.
3. **Fri 11 Dec:** the exam runs once. The result is reported as it comes out.

A missed bar is a finding, not a failure.

## After the exam

- Fixes made after the run are listed as "after the exam" and are not scored again.
- **Failure analysis:** each lane takes 5 to 10 real failures and shows input, output,
  truth, cause, and the fix or why there is none.
- **Cards:** each model piece gets one page on its training data, test set, number, known
  limits and intended use.

## The results table we will fill in

```
Sealed exam: 25 acts (n = .. with company tables), labelled blind, split by case,
run once at tag holdout-freeze (2026-12-11), provider and model: .. .

Main number: company tables fully correct among accepted acts
| System      | Correct  | Coverage | 95 % interval |
| Parser only | .. of .. | 100 %    |               |
| Model only  | .. of .. | 100 %    |               |
| Combined    | .. of .. | .. %     |               |

For information: product codes .., dates .., origins .., quote gate .. %,
planted errors caught .. of 20. Model-written numbers outside quotes: 0.
Cost per act .. EUR, slowest 5 % of acts above .. s.
Name matcher: .. right when deciding alone (baseline ..), .. % sent to a person, n = .. pairs.
Scope judge: .. of .. correct, .. missed, .. not sure, n = .. pairs from .. acts.
```

Every ".." is empty on purpose. We have no results yet. An earlier review of the idea
showed a mock-up of such a table with made-up scores. If you ever meet those numbers,
they are not ours.
