# Example 01: One case, four documents

**The side it shows:** time. A duty does not appear in one day. It grows through four
documents over 13 months. The ledger must be right on every one of those days.

All four documents are real. Bergmann's side is `[INVENTED]`.

## Step 1. Mon 15 Sep 2025: a notice

The Commission publishes notice C/2025/5010. It says: we start an anti-dumping
investigation on PET spunbond from China.

What the desk stores:

```
notice
  celex          the notice's id
  title          "Notice of initiation of an anti-dumping proceeding concerning imports
                  of PET Spunbond originating in the People's Republic of China"
  date           2025-09-15
  notice_type    initiation
  linked_measure (empty: there is no measure yet)
```

What Thomas sees: in the Must scope, nothing yet. Showing notices as early warnings is a
Could item (B-18). Thirteen months of warning is exactly what the third product bet is about.

There is no measure yet, so the desk shows no euro figure.

## Step 2. Tue 2 Dec 2025: registration

Regulation (EU) 2025/2409 tells customs to register these imports. It enters into force
the next day, 3 Dec 2025.

The act is short. Its Article 1(2) says:

> "Registration shall expire nine months following the date of entry into force of this
> Regulation."

What the ledger holds:

```
measure #1
  kind            AD
  stage           registration
  status          registered_only
  origin_countries  China
  legal_act_celex   32025R2409
  valid_from      2025-12-03
  valid_to        (empty)
measure_rate      (no rows: a registration has no rates)
measure_product   5603 13 90 (ex, TARIC 5603 13 90 70), 5603 14 20, 5603 14 80 (ex, TARIC 5603 14 80 70)
```

What Thomas sees on line L01: **"Registered: duty may be collected later."**

- The euro figure does not count it. Registration is a state, not a duty.
- Why it still matters: goods that enter while registration runs can be charged later, but
  only if a later act orders it. Thomas now knows his December shipments carry that risk.

A detail for lane B: the title of this act says "registration", which sounds harmless.
The desk still reads the whole act. The triage rule is: a registration act always goes to
full extraction.

## Step 3. Wed 13 May 2026: provisional duty

Regulation (EU) 2026/1063 sets a provisional duty. In force from 14 May 2026.

| Company | Provisional rate | Code |
|---|---|---|
| Hubei Unibon nonwovens Co Ltd | 45,6 % | 88CB |
| Changde Tiandingfeng Nonwovens Co Ltd; Tiandingfeng Nonwovens Co Ltd | 50,0 % | 88CC |
| Other cooperating companies | 49,4 % | see annex |
| All other imports originating in China | 50,0 % | 8999 |

Two more things this act does:

- Article 1(4): the goods are released only against "a security deposit equivalent to the
  amount of the provisional duty". Bergmann does not pay for good. It provides a security.
- Article 3(1): customs must "discontinue the registration of imports".

What the ledger holds now:

```
measure #1   stage registration   status superseded   superseded_by #2   valid_to 2026-05-14 (stated: the new act ends the registration)
measure #2   stage provisional    status in_force     valid_from 2026-05-14
             valid_to (empty)     valid_to_basis provisional_max
measure_rate for #2: the four rows above (see example 02 for how the annex row unfolds)
```

What Thomas sees on line L01: a range, because nobody has confirmed the producer's name yet.

- lowest: 400,000 x 45,6 % = **182,400 euros**
- highest: 400,000 x 50,0 % = **200,000 euros**
- with the note: "provisional: this amount is secured, not paid for good".

## Step 4. Fri 30 Oct 2026: definitive duty

Regulation (EU) 2026/2393. In force from Sat 31 Oct 2026. This is the Friday of our story.

| Company | Definitive rate | Code |
|---|---|---|
| Hubei Unibon nonwovens Co Ltd | 39,8 % | 88CB |
| Changde Tiandingfeng Nonwovens Co Ltd; Tiandingfeng Nonwovens Co Ltd | 48,1 % | 88CC |
| Other cooperating companies | 47,1 % | see annex |
| All other imports originating in China | 48,1 % | 8999 |

Every rate went down between May and October. That happens: the Commission keeps
calculating between the two stages.

Article 2 settles the amounts secured since May:

> "The amounts secured by way of the provisional anti-dumping duty under Commission
> Implementing Regulation (EU) 2026/1063 shall be definitively collected. The amounts
> secured in excess of the definitive rates of the anti-dumping duty shall be released."

And the December question from step 2 gets its answer. In its reasons, the act says the
conditions for collecting backwards "were not met". So nothing is charged for the goods
that entered during registration.

What the ledger holds now:

```
measure #2   stage provisional   status superseded   superseded_by #3
measure #3   stage definitive    status in_force     valid_from 2026-10-31
             valid_to (empty)    valid_to_basis expected_5y
act_conditions for 32026R2393
  invoice_declaration_required    yes
  provisional_collection_quote    "shall be definitively collected ... in excess ... shall be released"
  retroactive_collection_quote    (none in the operative part; the reasons say the conditions were not met)
```

What Thomas sees on line L01: **159,200 to 192,400 euros**, at last year's volumes, and one
open decision about the producer's name.

## What the same line looked like on four dates

| Date | State of the measure | Euro figure on L01 |
|---|---|---|
| 1 Oct 2025 | investigation running, no measure | none |
| 1 Jan 2026 | registered only | none, with the note "duty may be collected later" |
| 1 Jul 2026 | provisional, in force | 182,400 to 200,000, secured |
| 2 Nov 2026 | definitive, in force | 159,200 to 192,400 |

## Why the ledger never invents an end date

A definitive measure normally runs five years. So this one is "in force, expected to run
to about the end of October 2031 unless a review is open". The ledger stores no end date,
because no document states one. Example 08 shows a real measure that lived a full year
past its five years, which is why.

## What each lane takes from this

- **Lane B:** one case creates three measure rows that replace each other. The tests in
  issue B-07 should use exactly these three acts.
- **Lane A:** the definitive act points back at two earlier acts by number. "Which older
  act does this change" is a field the model must fill, with a quote.
- **Lane C:** the case page must say "secured", "registered" and "at last year's volumes"
  in the right places. The wrong word here is a wrong fact.
