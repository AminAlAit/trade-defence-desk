# Example 10: From a click to the proof

**The side it shows:** the sixth question, "Can I prove it?" What the desk saves when
Thomas decides, and what he can hand to his boss or an auditor.

The act is real. Bergmann's side, every decision and reason, and all timestamps are
`[INVENTED]`. The real producer appears only with the rate the public act gives it.

You saw this click at the kickoff. This example shows what happens behind it.

## Monday 2 Nov 2026, 09:10

Thomas opens the desk. The decisions list has three open questions, sorted by the money
they move:

| # | Question | Line | Moves |
|---|---|---|---|
| 1 | Is this product outside the act's scope? The desk proposes: yes. | L03 | up to 40,885 euros |
| 2 | Is the producer on your invoice the same legal entity as the one in the act? | L01 | 33,200 euros |
| 3 | Is the producer on your invoice the same legal entity as the one in the act? | L02 | 1,200 euros |

(40,885 is 85,000 x 48,1 %: what L03 would cost at the highest rate if it were in scope.)

For question 1 Thomas first wants to look at the product sheet. So he starts with question 2.

## He answers question 2

The screen shows both spellings side by side, the row of the duty table, and the sentence
of the act.

```
On your invoice:   Hubei Unibon Non-Woven Co., Ltd.
In the act:        Hubei Unibon nonwovens Co Ltd      39,8 %   code 88CB

[ Yes, the same legal entity ]   [ No ]   [ Not sure ]

Reason (required): ______________________________________
```

He picks "Yes" and writes a reason. The reason is required. "Yes" without a reason cannot
be saved.

## What is saved

One row in `decision`:

```json
{
  "id": 41,
  "match": 7,
  "question": "same_legal_entity",
  "answer": "yes",
  "reason": "Business licence number on the supplier's 2025 contract matches the company registered at the address in the invoice declaration.",
  "decided_by": "thomas",
  "decided_at": "2026-11-02T09:14:31+01:00"
}
```

And one row in `audit_event`, which is never changed or deleted afterwards:

```json
{
  "id": 1203,
  "ts": "2026-11-02T09:14:31+01:00",
  "actor": "thomas",
  "kind": "decision_made",
  "payload": {
    "decision_id": 41,
    "line": "L01",
    "measure": "AD, PET spunbond, China (32026R2393)",
    "before": {"low_eur": 159200, "high_eur": 192400},
    "after":  {"low_eur": 159200, "high_eur": 159200}
  }
}
```

The log records what the figure was before and after. Later, anyone can see why the
number changed on that Monday, and who changed it.

## What if he changes his mind?

On Wednesday the supplier writes: the fleece now comes from a sister factory.

Thomas does not edit decision 41. He makes a new one: "No", with the new reason. The log
then holds both, in order. The range opens again to 159,200 to 192,400, and the screen
shows that the answer was changed and when.

This is the same rule as in our decisions file: add a row, never rewrite one.

## "Continue unverified"

Sometimes Thomas has to move on without an answer. The scope question on L03 is waiting
for a data sheet. He can choose "continue unverified".

- A reason is required here too.
- The line keeps its range.
- The case shows "1 open point accepted as unverified" for everyone who opens it.

The desk lets a person carry a risk. It does not let the risk disappear.

## The proof export

One click gives one Markdown file per case. Shortened:

```markdown
# Evidence: PET spunbond from China, Bergmann Outdoor GmbH

Exported 2026-11-02 09:20. Desk version 1.0.0. Act text fingerprint: sha256 (64 characters)

## The act
Commission Implementing Regulation (EU) 2026/2393 of 29 October 2026
Published 30.10.2026. Applies from 31.10.2026 (the day after publication, Article 4).

## Facts used, each with its sentence
| Fact | Value | Source | Checked by |
| Rate for code 88CB | 39,8 % | Article 1(2), duty table | parser, confirmed by model |
| Rate for code 8999 | 48,1 % | Article 1(2), duty table | parser, confirmed by model |
| Invoice declaration needed | yes | Article 1(3): "shall be conditional upon presentation ..." | quote found |

## Your lines
| Line | Customs value last year | Rate used | Would cost at last year's volumes |
| L01 | 400,000 EUR | 39,8 % | 159,200 EUR |

## Decisions
| When | Who | Question | Answer | Reason |
| 2026-11-02 09:14 | thomas | same legal entity, L01 | yes | Business licence number ... |

## Assumptions
- Volumes: last full year. Not a forecast.
- Customs value: as uploaded, no freight assumption applied on L01.

## Not checked
- Not checked against TARIC.
- The desk did not verify the origin of the goods.
- Not legal advice. The Official Journal is the only authentic text.
```

Three things to notice:

1. **Every number has a source.** The export is built by code from the database. A model
   writes none of it.
2. **"Not checked" is part of the proof.** An auditor trusts a document more when it says
   where it stops.
3. **The version and the fingerprint** tie the export to one exact text of the act. If the
   EU later corrects the act, the fingerprint changes, and the export says which version
   Thomas decided on.

## Why this matters more than it looks

Without the log, the desk is a calculator: it shows a number and Thomas has to believe it.
With the log and the export, the desk is a record: Thomas can show how the number came
about, who decided what, and what nobody checked. For a head of customs, that is often
worth more than the number.

## What each lane takes from this

- **Lane C:** this example is issues C-05 (decisions and log), C-06 (highlighted quotes)
  and C-12 (export) in one story.
- **Lane A:** "checked by" in the export comes straight from `field_check`. The fingerprint
  comes from the stored act.
- **Lane B:** the `sha256` of each act is written once at download and never recomputed
  from changed text (issue B-02).
