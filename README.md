# Trade Defence Desk

A capstone project by three students of an AI and ML engineering bootcamp.
It runs from Mon 23 Nov to Fri 18 Dec 2026.

This repository is the team's shared memory. Right now it holds the plan, not the code.
The code arrives during week 1, in this same repository.

## The idea in five sentences

1. The EU sometimes puts an extra duty on a product from one country, for example a polyester fleece from China.
2. The rate is different for each producer, and it is written in a legal text called an act.
3. An importer in Germany often learns about a new act late, and then searches a long text by hand for its supplier's name.
4. Our desk reads every new act on the day it is published and turns it into checked facts.
5. It compares those facts with the importer's own purchases and shows what is at stake in euros, with the sentence behind every number.

## Our importer

We tell the whole project through one invented company:

- **Bergmann Outdoor GmbH**, Erfurt. It sells garden and camping goods.
- **Thomas** is its head of customs. He is the person the desk is built for.
- Bergmann buys from factories outside the EU on about 20 purchase lines.

Bergmann and Thomas are invented. The acts they meet are real and public.

## Read in this order

| Step | File | What you learn | Time |
|---|---|---|---|
| 1 | [docs/01_PRODUCT.md](docs/01_PRODUCT.md) | what the desk does, for whom, and what it is not | 10 min |
| 2 | [docs/02_GLOSSARY.md](docs/02_GLOSSARY.md) | the trade words, in plain language | 10 min |
| 3 | [docs/examples/](docs/examples/README.md) | ten worked examples built on real acts | 60 min |
| 4 | [docs/03_SCOPE.md](docs/03_SCOPE.md) | what we build in four weeks, and what we leave out | 5 min |
| 5 | [docs/04_ARCHITECTURE.md](docs/04_ARCHITECTURE.md) | the diagram, coloured by lane | 10 min |
| 6 | [docs/08_LANES_AND_ROLES.md](docs/08_LANES_AND_ROLES.md) | the three lanes and who answers for what | 10 min |
| 7 | [docs/09_ROADMAP.md](docs/09_ROADMAP.md) | the four weeks and the four Fridays | 5 min |

Then read what your lane needs:

| File | What it holds |
|---|---|
| [docs/05_DATA_SCHEMA.md](docs/05_DATA_SCHEMA.md) | every table of the database (the ledger), with a diagram |
| [docs/06_AI_RULES.md](docs/06_AI_RULES.md) | what the model may do, and what only Python or a person may do |
| [docs/07_TECH_STACK.md](docs/07_TECH_STACK.md) | the tools, why each one is here, and the ones we left out |
| [docs/10_EVALUATION.md](docs/10_EVALUATION.md) | how we know the desk works: the sealed exam and the numbers |
| [docs/11_DECISIONS.md](docs/11_DECISIONS.md) | what is already decided, with one line of why |
| [docs/12_WORKING_AGREEMENT.md](docs/12_WORKING_AGREEMENT.md) | branches, reviews, what "done" means, the weekly rhythm |
| [docs/13_SOURCES.md](docs/13_SOURCES.md) | where the acts come from, and links for your own research |
| [docs/14_RISKS.md](docs/14_RISKS.md) | what could sink the project, and what we do about it |
| [docs/15_COMPETITORS.md](docs/15_COMPETITORS.md) | who else does something similar, and the gap we fill |
| [docs/16_BACKLOG.md](docs/16_BACKLOG.md) | all 73 work items; each one is also a GitHub issue |
| [docs/17_DEMO_AND_PRESENTATION.md](docs/17_DEMO_AND_PRESENTATION.md) | the plan for the final presentation |
| [data/sample_acts/](data/sample_acts/README.md) | four real acts to open and read: three from one case, one very different |
| [prototype/](prototype/README.md) | the clickable prototype the frontend starts from |

## Your first day

1. Read steps 1 to 3 of the table above. That is about 80 minutes.
2. Open the prototype in [prototype/](prototype/README.md) and click through one case.
3. Unpack one real act from [data/sample_acts/](data/sample_acts/README.md) and find its Article 1.
4. Open the issues, filter by your lane and by the milestone "M1", and read those issues.
5. Check that Docker Desktop and `uv` run on your laptop.
6. Write down what you still do not understand, and bring it to the next standup.

## The work

- Every work item is a **GitHub issue**, labelled with its lane, its priority and its size.
- The issues are grouped into **milestones**, one per Friday.
- To take an item, assign yourself to the issue.
- The id of an item starts with a letter: **A**, **B** or **C** for the lane, **X** for
  shared work, **K** for extras.
- **Must** means the capstone fails without it. **Should** is dropped first if we are
  behind. **Could** is an extra. More in [docs/03_SCOPE.md](docs/03_SCOPE.md).

## The small tags behind facts

| Tag | Meaning |
|---|---|
| `[MEASURED date]` | someone ran a test and wrote down the result |
| `[LAW act, article]` | read in the legal text |
| `[EST]` | an estimate |
| `[VERIFY]` | not checked yet; treat it as open |
| `[INVENTED]` | made up for the story or for teaching |

## Asking an AI assistant about this project

[CLAUDE.md](CLAUDE.md) tells an AI assistant how to read this repository and which words to use.
If you connect this repository to your assistant, point it at that file first.

## Three things this project never claims

- **It is not legal advice.** The Official Journal of the EU is the only authentic text.
- **It is not checked against TARIC.** We found no free, structured TARIC feed. The desk checks each fact against the act's own text.
- **The euro figures are not a forecast.** They always mean "what this would cost at last year's volumes".

## Sources and reuse

The act texts come from the Publications Office of the European Union, with attribution.
The exact reuse terms are still marked `[VERIFY]` in [docs/13_SOURCES.md](docs/13_SOURCES.md).
