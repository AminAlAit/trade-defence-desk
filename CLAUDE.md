# Notes for an AI assistant reading this repository

You are helping one of three bootcamp students understand and build the Trade Defence Desk.
They are learners. Explain in plain language, with short sentences, and one idea at a time.

## How to find things

| Question | Read |
|---|---|
| What is this project? | `README.md`, then `docs/01_PRODUCT.md` |
| What does a trade word mean? | `docs/02_GLOSSARY.md` |
| Show me a concrete case | `docs/examples/` (ten worked examples) |
| Is this in scope? | `docs/03_SCOPE.md` |
| How do the parts connect? | `docs/04_ARCHITECTURE.md` |
| What is in the database? | `docs/05_DATA_SCHEMA.md` |
| May the model do this? | `docs/06_AI_RULES.md` |
| Which tool, and why? | `docs/07_TECH_STACK.md` |
| Whose job is this? | `docs/08_LANES_AND_ROLES.md` |
| When is it due? | `docs/09_ROADMAP.md` |
| How is it tested and scored? | `docs/10_EVALUATION.md` |
| Was this already decided? | `docs/11_DECISIONS.md` |
| How do we work together? | `docs/12_WORKING_AGREEMENT.md` |
| Where does the data come from? | `docs/13_SOURCES.md` |
| What is the work item? | `docs/16_BACKLOG.md` and the GitHub issues |

When you answer, name the file and the heading you used.
If the repository does not answer the question, say so. Do not fill the gap with a guess.

## Words to use

These rules come from our own review of the wording against the legal texts. No customs
professional has confirmed them yet. They apply to code, UI text, docs and slides.

| Say | Never say | Why |
|---|---|---|
| duty, anti-dumping duty | tax | "tax" collides with import VAT |
| the same legal entity as the producer named on the invoice | the same company | the rate follows the producer named on the invoice |
| would cost, at last year's volumes | will cost | the figure is not a forecast |
| the duty rate for (company) | the duty is X % | a rate belongs to one company and one price base |
| excluded from the act's scope | exempt, exemption | "exemption" is the law's word for something else |
| no matching measure found in the acts we read | no duty, not affected | the desk does not read TARIC or every notice |
| in force, expected to run to DATE unless a review is open | in force until DATE | a measure stays in force while a review runs |
| registered: duty may be collected later | new duty | registration is not a duty yet |
| name decided, no open decision | final | the amounts still rest on assumptions |
| all other imports; other cooperating companies | "residual" alone | they are two different fallback rates |
| the duty rate for (company), on the net, free-at-Union-frontier price | a rate without its company and its price base | the rate belongs to one company and one base |
| extension, scope exclusion, exemption: three words | one word for all three | they are three different legal things |
| duty on shipments arriving soon, to pay or secure, if they are released after the act applies | cash due this week | the duty applies when customs releases the goods |
| the supplier has an accepted price undertaking: no duty if the invoice conditions are met | exempt | an undertaking is its own legal instrument |
| interested parties may comment by (date) | comments due | an importer that is not a registered party cannot simply comment |
| this act lists China as origin; we found no duty in it for goods made in (other country); check for an extension | (other country) has no duty | origin, dispatch and extensions differ |

Also:

- Never write "checked against TARIC".
- Never put "EU" in the product name, and never use the EU emblem.
- Do not use em-dashes or en-dashes in this repository.
- The sealed test set is called "the sealed exam". The set we tune on is called "the practice set".
  The glossary mentions the engineering word "holdout" once, and the git tag is `holdout-freeze`.

## Facts and their labels

The docs mark how sure a fact is:

- `[MEASURED date]`: someone ran a probe and wrote down the result.
- `[LAW act, article]`: read in the legal text.
- `[EST]`: an estimate.
- `[VERIFY]`: not checked yet. Treat it as open.
- `[INVENTED]`: made up for the story or for teaching.

Keep these labels when you repeat a fact. Never turn an `[EST]` or `[INVENTED]` number into a plain fact.

## Hard rules of the product

1. No number the user sees comes from free model text. See `docs/06_AI_RULES.md`.
2. The sealed exam is run once. Two people label it. Whoever builds the extraction never sees it. See `docs/10_EVALUATION.md`.
3. The importer is always synthetic. No real customer data, ever.
4. The scope is fixed. A new idea goes through the scope guard in `docs/03_SCOPE.md`.

## What is real and what is invented

- Real: the acts, their numbers, their producer names, their dates. Four acts are in `data/sample_acts/`.
- Invented: Bergmann Outdoor GmbH, Thomas, Bergmann's purchases and euro amounts, and any act marked `[INVENTED]`.
- Not yet existing: every result. Any score in `docs/examples/` is an illustration, not a result of ours.
