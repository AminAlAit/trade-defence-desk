# 01 Product: what the Trade Defence Desk is

## In one sentence

The Trade Defence Desk reads every new EU trade defence act on the day it is published,
turns it into checked facts, compares them with an importer's own purchases, and shows
what is at stake in euros. Every number links to the sentence it came from, and every
uncertain point goes to a person.

New words? They are in [02_GLOSSARY.md](02_GLOSSARY.md). Tags such as `[EST]` or `[VERIFY]`
behind a fact say how sure it is; the key is in the [README](../README.md).

## The problem

- **Duties are set per company.** One act lists several producers, each with its own rate.
  A producer the act does not name pays a fallback rate, which is often higher.
- **The company rate has a condition.** It applies only if the invoice carries a signed
  declaration with exact wording. Without it, the fallback rate applies
  `[LAW 2026/2393, Art 1(3)]`.
- **Acts arrive often, in bursts.** 14 regulations in the 30 days to 13 Nov 2026, and 103
  in 12 months `[MEASURED 2026-11-13]`. That is roughly one act every second working day,
  and often several on the same day.
- **Importers find out late.** Often through a forwarder's circular or an association
  email. Then someone searches a long act by hand for producer names that appear in several
  spellings `[EST]`.

The size of this pain is an estimate until we talk to a real customs person. Issue X-07
sets up that conversation.

## Who it is for

- **First:** the head of customs at a German mid-sized importer. Ours is Thomas at
  Bergmann Outdoor GmbH `[INVENTED]`.
- **Also:** customs brokers and freight forwarders who serve many importers, and
  purchasing teams.
- **Not for:** lawyers writing defence submissions, or exporters outside the EU.

## What Thomas gets: six questions, always in this order

| # | Question | What the desk shows |
|---|---|---|
| 1 | What happened? | which act, which product, which countries, which stage, from when |
| 2 | Does it hit me? | which of my purchase lines are covered |
| 3 | How much? | the extra duty at last year's volumes; a range while a decision is open |
| 4 | What do I decide? | one list: producer names to confirm, possible exclusions, unreadable cells |
| 5 | What next? | a checklist, and drafts filled from templates |
| 6 | Can I prove it? | every number links to its sentence; a log of decisions; an export |

Every case page answers these six, in this order.

## How it works, in eight steps

Each step says who does the work: Python code, fixed rules, a language model, a template
or a person.

| # | Step | Who does it | What Thomas sees |
|---|---|---|---|
| 1 | Fetch the act | python | act number, size, "text complete" |
| 2 | Recognise the type of act | rules on the title | "Definitive anti-dumping duty, PET spunbond, China" |
| 3 | Read the duty table | python | company rows by kind, grouped cells resolved |
| 4 | Read scope and dates | model | product codes, dates, each with its quote |
| 5 | Check every field against the act's text | python | "14 confirmed, 1 to check" |
| 6 | Match with Bergmann's lines and producers | python; the model for hard cases; a person decides | hits and uncertain matches |
| 7 | Compute the euros at stake | python | a range at last year's volumes |
| 8 | Write tasks and drafts | template | no number written by the model |

The architecture diagram in [04_ARCHITECTURE.md](04_ARCHITECTURE.md) cuts the same work
into 13 numbered boxes. It has a table that maps these eight steps to those boxes.

The worked examples in [examples/](examples/README.md) walk through these steps with real data.

## What it is not

- **Not legal advice.** The Official Journal is the only authentic text.
- **Not checked against TARIC.** No free, structured TARIC feed was reachable in three
  attempts `[MEASURED 2026-11-13]`. The desk checks against the act's own text, the list
  of product codes, and its own consistency.
- **It does not decide where goods come from.** It says which test applies. A person decides.
- **Not a forecast.** Euro figures are always "at last year's volumes".
- **No safeguards.** Safeguards are a different kind of measure with no company rates.
  The desk shows them but does not apply them.

## Three bets we have not tested yet

The first idea was only an alert: "your supplier now carries a higher rate". The prototype
added three bets. Each needs a real customs person to confirm it (issue X-07):

1. Thomas cares about euros on his own purchase lines.
2. The desk saves hours compared with reading by hand.
3. The desk gives days of warning.

## Domain facts we rely on

Read from the legal texts on 2026-11-21. The basic regulation has been amended since the
version we read, so issue X-06 rechecks all of them against the current text before any of
them appears in the UI.

| # | Fact | Source |
|---|---|---|
| 1 | Provisional anti-dumping duties last six months, and can be extended to nine. | `[LAW 2016/1036, Art 7(6)]` |
| 2 | A definitive duty can reach back at most 90 days before the provisional duty, only for registered goods, and only if the act orders it. | `[LAW 2016/1036, Art 10(4), 14(5)]` |
| 3 | Definitive measures end after five years unless an expiry review is opened. They stay in force while the review runs. | `[LAW 2016/1036, Art 11(2)]` |
| 4 | The company rate depends on an invoice declaration that each act words itself. | `[LAW 2026/2393, Art 1(3)]` |
| 5 | Provisional duties are secured by a guarantee, not paid for good. | `[LAW 2016/1036, Art 7(3)]` |
| 6 | When a definitive duty follows a provisional one, the lower of the two rates counts for the goods already released. The act says so in its own words. | `[LAW 2016/1036, Art 10(3)]` |
| 7 | One product can carry an anti-dumping and an anti-subsidy duty at the same time, but not both for the same situation. | `[LAW 2016/1036, Art 14(1)]` |
| 8 | Who owes the duty at the border (the importer, its customs agent, or the supplier) is not in these regulations. It is in the Union Customs Code, which we have not read yet. | `[VERIFY]` |

The three basic regulations: (EU) 2016/1036 on dumped imports, (EU) 2016/1037 on
subsidised imports, and (EU) 2015/478 on common rules for imports, which holds the
safeguards.
