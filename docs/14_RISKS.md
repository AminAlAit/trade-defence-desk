# 14 Risks

What could sink the project, and what we do about it. "Chance" and "damage" are our own
estimates `[EST]`. The watcher raises the risk at the Friday review.

| # | Risk | Chance | Damage | What we do | Watched by |
|---|---|---|---|---|---|
| R1 | **Nothing moves in the demo.** A new act comes only about every second day. | high | high | The replay of stored runs, marked "replay", ready by M2. Then the newest real act live. | lane C |
| R2 | **Later acts change earlier ones.** The product is a ledger of measures over time, not a list of acts. Applying a change correctly is the hardest modelling job. | high | high | We handle registration, provisional to definitive, repeal, and "in force while a review runs". Everything else goes to a person. We never compute an end date. | lanes B, A |
| R3 | **Table traps:** grouped cells, decimal commas, invisible spaces, 196 tables in one act. | high | medium | The parser is built first, with tests on the real act. Parser and model are compared on every rate. | lane A |
| R4 | **Names:** spelling variants, "Co Ltd" variants, related companies in one row, a trader who is not the producer. | medium | high | Match the producer on the invoice. All names of a row are kept. A person decides below the safe threshold. Hard look-alikes in the test pairs. | lane B |
| R5 | **TARIC is not available**, so "checked against TARIC" is tempting but false. | certain | medium | The claim is banned. We say what we do check against. | all |
| R6 | **We fool ourselves in the evaluation** by tuning on the test acts. | medium | high | The sealed exam: split by case, hidden, labelled by two people, promise written first, run once. | lanes B, A |
| R7 | **Model cost or limits** on free tiers. | medium | high | Measure 3 acts on Tue 24 Nov. Send only the operative part. Cache answers. A small capped budget if needed. | lane A |
| R8 | **The EU changes its format**, or the endpoint is down. | low | high | Raw acts are stored in the repository with fingerprints, so the evaluation never needs the live endpoint. | lane B |
| R9 | **Our wording claims more than the tool knows** ("will cost", "no duty", "in force until"). | medium | high | The wording rules. Rechecking the domain facts against the current law (X-06). A domain review of the screens before M3. | lane C |
| R10 | **Scope creep:** more countries, WhatsApp, news, before the core works. | high | high | The scope guard. Extras only after M3, one owner each. | all |
| R11 | **One lane blocks the others.** | medium | high | Data shapes frozen on Thu 26 Nov. Example files for every shape from day 1. | lane A |
| R12 | **Uneven load, or someone is out.** The Must list is already above our capacity. | high | high | Rebalance every Friday. The shrink order is written down. Each model piece can shrink without disappearing. | all |
| R13 | **Our hand-written answers are wrong.** We are not customs experts. | medium | medium | A labelling guide with examples. Some acts are labelled twice and compared. One hour with a customs person, if we find one. | lanes B, A |
| R14 | **Hosting surprises** on presentation day. | medium | medium | Check the free-tier limits. Create the online database in week 3. Wake the service before the demo. The laptop version and the backup video are the fallbacks. | lane A |
| R15 | **A heavy job freezes a laptop.** | medium | low | Small sample first, one job at a time. | lane B |
| R16 | **Someone reads the desk as legal advice.** | low | medium | The footer and the export say what the desk is not. | lane C |
| R17 | **Real producer names appear next to an invented importer** and look like an accusation. | low | low | The importer is marked as invented everywhere. Producer names come from public acts and only show how matching works. | lane B |
| R18 | **Too few acts of the kind we need.** Only about a third set duties. | high | high | 24 months of acts. Real counts on Tue 24 Nov. At least 12 acts with company tables in the exam. | lane B |

The Friday warning signs are in [09_ROADMAP.md](09_ROADMAP.md).
