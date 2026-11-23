# Example 08: A quiet day, and an act without a table

**The side it shows:** most acts do not hit Bergmann, and not every act looks like the
fleece act. The desk has to handle both without noise.

The act is real: Regulation (EU) 2026/2311, published Tue 20 Oct 2026.

## The act

Its title, shortened: "imposing a definitive anti-dumping duty on imports of certain
heavyweight thermal paper originating in the Republic of Korea following an expiry review".

Heavyweight thermal paper is a coated paper that turns dark where a printer heats it. The
act says it is "mainly used for self-adhesive labels for packaging". It is sold in very
large rolls.

Its whole Article 1(2) is one sentence:

> "The rate of the definitive anti-dumping duty applicable to the net, free-at-Union-frontier
> price, before duty, of the product described in paragraph 1, shall be 15,8 %."

No company names. No table. No annex. No invoice declaration. One rate for everything from
Korea.

## What that means for each part of the desk

| Part | With the fleece act (2026/2393) | With this act (2026/2311) |
|---|---|---|
| Triage | "definitive duty" | "definitive duty, after an expiry review" |
| Duty-table parser | 4 visible rows, 8 codes | **finds no duty table, and that is correct** |
| Model | scope, dates, earlier acts | scope, dates, earlier acts, **and the rate sentence**, with its quote |
| Ledger | 8 `measure_rate` rows in 3 kinds | **1 row**, kind `country_wide`, 15.8 |
| Name matcher | needed | **not needed**: no names |
| Euro engine | a range until the name is decided | one figure at once |

The important line is the second one. A parser that returns nothing must be able to say
which of two things happened:

- "there is no company table in this act" (correct here), or
- "there is a table and I could not read it" (a failure).

The first is a result. The second goes to a person. If the two look the same, the desk is
silently wrong on every act like this one.

This is also why the act is one of our two fixed example acts. It is the opposite of the
fleece act in almost every way.

## A measure that outlived its five years

The history of this measure, from the act's own footnotes:

| Date | Document | What happened |
|---|---|---|
| Tue 20 Oct 2020 | Regulation (EU) 2020/1524 published | the definitive duty starts |
| Mon 3 Feb 2025 | Notice C/2025/680 | a notice of impending expiry: the measure will end soon unless a review is asked for |
| Fri 17 Oct 2025 | Notice C/2025/5537 | an expiry review starts |
| Tue 20 Oct 2026 | Regulation (EU) 2026/2311 published | the duty continues |

Five years after October 2020 is October 2025. A ledger that computes "start plus five
years" would have closed this measure in late October 2025.

That would have been wrong for a full year. The review notice of 17 Oct 2025 came a few
days before the five years ended, and a measure stays in force while its review runs.

What our ledger holds instead:

| On this day | `status` | What the case says |
|---|---|---|
| 1 Jan 2025 | `in_force` | "in force, expected to run to about October 2025 unless a review is open" |
| 1 Mar 2025 | `in_force`, `has_open_event` | the same, plus a note that a notice of impending expiry was published |
| 1 Nov 2025 | `under_review` | "in force while an expiry review runs" |
| 1 Nov 2026 | a new measure, `in_force` | "in force, expected to run to about October 2031 unless a review is open" |

Two short notices changed the truth about this measure. Neither of them contains a rate
or a company. That is why the Must scope stores the titles and dates of notices and links
them to measures (issue B-13), even though it does not read the notices in full.

## What Bergmann sees

Bergmann sells garden and camping goods. It buys no thermal paper.

- The act is in the ledger, fully read.
- Thomas's inbox shows no new case.
- If he opens the list of all acts, this one says: **"no matching measure found in the
  acts we read"**, for each of his lines.

It does not say "you are not affected". The desk compared the act with the lines Bergmann
uploaded. It does not know what Bergmann forgot to upload.

## The other quiet lines

Three of Bergmann's lines match nothing in any of the ten examples:

| Line | What the desk says |
|---|---|
| L05 plywood from Brazil | "no matching measure found in the acts we read" |
| L06 e-bike motors from China | the same |
| L08 solar garden gnomes from China | the same |

This is the normal state. In the synthetic importer, about a third of the lines fall under
a real act, and the rest are there on purpose: decoys. A desk that finds something on
every line is a desk that cries wolf.

## How triage reads a title

Triage only looks at the title. Four real titles, shortened:

| Title says | Type |
|---|---|
| "making imports of PET spunbond ... subject to registration" | registration |
| "imposing a provisional anti-dumping duty on imports of PET Spunbond ..." | provisional duty |
| "imposing a definitive anti-dumping duty and definitively collecting the provisional duty ..." | definitive duty |
| "imposing a definitive anti-dumping duty ... following an expiry review ..." | definitive duty, after an expiry review |

Titles are formal and regular, which is why plain rules do well here. The experiment in
issue B-15 checks whether a model does any better.

## The numbers behind "quiet"

In the 30 days to 13 Nov 2026 the EU published 14 trade defence regulations
`[MEASURED 2026-11-13]`:

| Kind | Count | Sets or changes a rate? |
|---|---|---|
| registrations | 5 | no |
| definitive duties | 3 | yes |
| provisional duties | 2 | yes |
| repeals | 2 | ends one |
| amendments | 2 | sometimes |

For one importer with 20 purchase lines, most weeks bring nothing. That is fine. The value
of the desk is that Thomas can trust the silence.

## What each lane takes from this

- **Lane A:** the parser returns a typed answer for "no company table", and the tests pin
  it on this act (issues A-02, X-17).
- **Lane B:** the triage rule for "following an expiry review" comes from the title. The
  ledger test for `under_review` can use the four documents above (issues B-05, B-07, B-13).
- **Lane C:** the inbox needs an honest empty state.
