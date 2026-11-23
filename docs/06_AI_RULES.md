# 06 The AI rules

What the language model may do, what only Python may do, and what only a person may do.
The code enforces these rules. They are not good intentions.

## Who does what

| Job | Python | Model | Person |
|---|---|---|---|
| Read the duty table (names, rates, codes) | does it | reads it a second time, as a cross-check | decides if the two disagree |
| Read scope, dates, "which older act does this change" | checks the model's answer | does it, with a quote for each field | sees what failed the check |
| Decide whether two producer names are the same legal entity | scores the pair | not involved | decides everything below the safe threshold |
| Decide whether a product is outside an act's scope | not possible | proposes, with a quote, or says "not sure" | confirms |
| Compute euros | does it | never | fills in assumptions |
| Write the tasks and drafts | fills templates | never writes a number | sends them |

## The six rules

### 1. No number the user sees comes from free model text

Rates, rows and euros come from the parser, the ledger or the euro engine.

- A value the model extracts, such as a date or a product code, appears only after the
  verifier has found it inside its own quote. Code renders it, not the model.
- Any other model text shown to a user passes the **number guard**: a digit outside a
  word-for-word quote fails an automatic test.
- Word-for-word quotes are allowed to contain digits, because they are the act's own words.

### 2. Python reads tables; the model checks them

If parser and model disagree on a rate, the field goes to a person. Neither side wins
silently.

### 3. Every model field carries a quote, and the quote must contain the value

Both are compared after cleaning up invisible spaces and decimal commas. If the check
fails, the field shows amber as "not verified".

### 4. The model gets the operative part and the annexes, not the recitals

This is a guess `[EST]`, so the experiment in issue A-13 tests it.

### 5. A person decides what a program cannot prove

Same legal entity, product outside the scope, unreadable cell. Every decision is saved
with a reason.

### 6. One declared setup for all reported numbers

One provider, one model and one prompt version per evaluation run, written down before
the run.

## Why so strict?

- A wrong rate costs a real importer real money. A fluent, confident, wrong sentence is the
  worst thing this product could produce.
- People tend to trust what a machine shows them. The amber states and the decisions list
  keep a person in the loop where the machine cannot be sure.
- For us as students, "the model never writes a number, and here is the test that proves
  it" is a stronger story than "we prompted carefully".

## How each rule is tested

| Rule | Test | Issue |
|---|---|---|
| 1 | the number guard runs on every pull request | C-17 |
| 2 | parser and model are compared on every rate; mismatches are counted | A-04, A-05 |
| 3 | 20 wrong values are planted by teammates who have not read the verifier; we count how many it catches | A-07 |
| 4 | operative part against full text, on the practice set | A-13 |
| 5 | every decision creates a log entry; a test checks it | C-05 |
| 6 | the setup is written into the pre-registration before the exam | X-10 |

See the rules at work in
[examples/03_THE_MODEL_AND_THE_QUOTE_GATE.md](examples/03_THE_MODEL_AND_THE_QUOTE_GATE.md).
