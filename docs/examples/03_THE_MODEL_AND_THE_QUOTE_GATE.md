# Example 03: The model and the quote gate

**The side it shows:** trust. The model reads what a table cannot say. Python then checks
every answer against the act's own words.

The quotes are real, from Regulation (EU) 2026/2393. The model answers are `[INVENTED]` to
show how the checks behave. We have not run a model on this act yet.

## What the model is asked

The model receives the operative part and the annex, not the 170 paragraphs of reasons.
For every field it must return two things: the **value**, and a **quote** copied word for
word from the act.

## Six answers, six checks

The check has two parts:

1. **Quote found?** Is the quote really in the act, word for word?
2. **Value inside the quote?** Does the quote contain the value?

Before comparing, Python cleans both sides the same way: special spaces become normal
spaces, and "39,8" and "39.8" count as the same number.

**Green** means: both parts passed. **Amber** means: not verified, a person should look.

| # | Field | The model's value | The model's quote | Check | Shown as |
|---|---|---|---|---|---|
| 1 | stage | definitive | "A definitive anti-dumping duty is imposed on imports of certain non-woven needle-punched sheets of polyester filaments" | found; "definitive" is in it | green |
| 2 | origin | People's Republic of China | "and originating in the People's Republic of China" | found; value is in it | green |
| 3 | product codes | ex 5603 13 90; 5603 14 20; ex 5603 14 80 | "currently falling under CN codes ex 5603 13 90, 5603 14 20 and ex 5603 14 80" | found; all three are in it; all three exist in the code list | green |
| 4 | what happens to amounts secured above the definitive rate | released | "The amounts secured in excess of the definitive rates of the anti-dumping duty shall be released." | found; value is in it | green |
| 5 | the provisional act this one follows | 2026/1036 | "under Commission Implementing Regulation (EU) 2026/1063" | found; **value is not in the quote** | **amber: not verified** |
| 6 | thickness limit of the product | not exceeding 1,8 mm | "of a thickness exceeding 0,5 mm but not exceeding 1,8 mm and coated" | **quote not found word for word** | **amber: not verified** |

### What went wrong in row 5

The model swapped two digits: 1036 instead of 1063. A person skimming would never notice.
The check notices at once, because "2026/1036" does not appear inside the quote.

(2016/1036 is the number of the basic anti-dumping regulation, which this act also cites.
Two real numbers that differ by one swap: exactly the kind of slip a model makes.)

### What went wrong in row 6

Compare the two:

| | Text |
|---|---|
| The act | "of a thickness exceeding 0,5 mm but not exceeding 1,8 mm, impregnated with one or more binders" |
| The model's quote | "of a thickness exceeding 0,5 mm but not exceeding 1,8 mm and coated" |

The act never says "and coated". A few words later it even says the opposite: "not coated
or covered". The model stitched a quote together. Those words are not in the act in that
order, so the quote is rejected.

Amber does not mean wrong. It means: nobody has confirmed this. The field goes on the
decisions list with the sentence the model pointed at.

## A harder case: a value that is not written anywhere

When does the act apply? Article 4 says:

> "This Regulation shall enter into force on the day following that of its publication in
> the Official Journal of the European Union."

The articles never write the date "31 October 2026". The date follows from a rule plus the
publication date (30 Oct 2026). That date stands in the header of the file and in the EU's
catalogue data, not in Article 4.

If the model answered "2026-10-31", the value-in-quote check would fail, correctly: that
date is not in the sentence it quotes.

So this field is split:

| Part | Who | Result |
|---|---|---|
| Which rule does the act use? | the model, with the quote above | "the day after publication" |
| What is the publication date? | Python, from the catalogue | 2026-10-30 |
| So the act applies from | Python | 2026-10-31 |

The model never does the date arithmetic. This is rule 1 of the AI rules: values the user
sees come from code. How exactly derived values are stored is for lane A to settle in
issue A-04.

## The planted-error test

How do we know the verifier catches mistakes? We plant some.

- The owners of lanes B and C write 20 wrong values into correct extractions, without
  reading the verifier's code.
- Lane A runs the verifier and counts how many it flags.

Examples of plants on this act:

| Plant | Should the verifier catch it? |
|---|---|
| the rate for 88CB changed from 39,8 to 38,9 | yes: the parser and the model disagree |
| the origin changed to "Republic of Korea", quote unchanged | yes: the value is not in the quote |
| a product code changed to 5603 14 99 | yes: that code does not exist in the code list |
| the quote for the stage shortened by a few words | no, and that is fine: the quote is still in the act and still contains the value |

The share caught is reported, for example "17 of 20" `[INVENTED]`. A verifier that catches
everything we plant is suspicious too, so the plants should be mean.

## The number guard

Some model text is shown to Thomas as explanation. That text may not contain a digit,
unless the digit is inside a word-for-word quote.

| Model text | Guard |
|---|---|
| "The rate for this producer went down compared with the provisional stage." | passes |
| "The rate for this producer went down by 5,8 points." | **fails**: a digit outside a quote |
| "The act limits the product to sheets 'of a thickness exceeding 0,5 mm but not exceeding 1,8 mm'." | passes: the digits are inside a quote that is in the act |

5,8 happens to be the true difference between 45,6 and 39,8. The guard does not care. If
Thomas should see that difference, Python computes it and a template prints it.

## What each lane takes from this

- **Lane A:** rows 5 and 6 are the two failure kinds the verifier must tell apart: "quote
  found, value missing" and "quote not found".
- **Lane B:** only green fields flow into the ledger. Amber fields wait.
- **Lane C:** an amber field needs a place on the case page and a line on the decisions
  list. The number guard (issue C-17) is yours.
