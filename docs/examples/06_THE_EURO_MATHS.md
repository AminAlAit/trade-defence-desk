# Example 06: The euro maths

**The side it shows:** money. Every sum behind the figure Thomas sees, including money
that comes back.

The rates are real, from Regulations (EU) 2026/1063 and 2026/2393. Every euro amount of
Bergmann is `[INVENTED]`.

The basic sum never changes:

```
extra duty = customs value x rate
```

Everything else is the question: **which value, and which rate?**

Nine sums follow. Sums 1 and 2 are the ones you saw at the kickoff. Sums 3 to 9 are new.

Every purchase and shipment below is invented. The two real producers appear only with
the rates the public act gives them.

## Sum 1: line L01, name not yet confirmed

Bergmann bought 400,000 euros of fleece on this line last year. The producer on the
invoice looks like Hubei Unibon, but nobody has confirmed it.

| If the producer is | Rate | Extra duty at last year's volumes |
|---|---|---|
| Hubei Unibon (code 88CB) | 39,8 % | 400,000 x 0.398 = **159,200 euros** |
| not confirmed (code 8999, all other imports) | 48,1 % | 400,000 x 0.481 = **192,400 euros** |

Thomas sees: **159,200 to 192,400 euros**. The range is 33,200 euros wide. That is what
one open decision is worth.

## Sum 2: Thomas confirms the name

He answers "yes, the same legal entity". The range becomes one number: **159,200 euros**.

But the low rate has a second condition. Article 1(3) says the individual rate applies only
if the invoice carries a signed declaration with fixed wording, and:

> "Until such invoice is presented, the duty applicable to all other imports originating
> in the People's Republic of China shall apply."

So the rule in the euro engine is:

| Producer confirmed? | Declaration on the invoice? | The desk shows |
|---|---|---|
| no | any | the range |
| yes | yes | the single low figure |
| yes | **no** | still the range, plus a task: "Ask the supplier for the invoice declaration" |

On L01 the declaration is there, so the figure is 159,200.

## Sum 3: line L02, the second source

Bergmann bought 120,000 euros through a trader. The producer on the invoice is Hebei
Saikefu, which is in the annex ("other cooperating companies").

| Rate | Extra duty |
|---|---|
| 47,1 % (annex, code 88CE) | 120,000 x 0.471 = **56,520 euros** |
| 48,1 % (all other imports) | 120,000 x 0.481 = **57,720 euros** |

Here the open decision is worth only 1,200 euros. The desk can sort the decisions list by
this number: the questions that move the most money come first.

Whether the annex rate also needs the invoice declaration is not settled in our reading of
the act `[VERIFY]`. Until a person has checked, the desk keeps the range.

## Sum 4: both lines together

| | Low | High |
|---|---|---|
| L01 | 159,200 | 192,400 |
| L02 | 56,520 | 57,720 |
| **Fleece in total** | **215,720** | **250,120** |

## Sum 5: what if the line only has an invoice value?

The duty is calculated on the customs value: the price at the EU border, with freight and
insurance. Some purchase lines only hold the price paid at the factory or the port of
shipment.

Then the engine uses a labelled assumption: **plus 8 %** for freight and insurance.

```
invoice value 100,000 euros  ->  assumed customs value 108,000 euros
```

The case page shows the assumption next to the figure, and Thomas can change it. An
assumption is never hidden inside a number.

## Sum 6: the containers at sea

36,000 euros of L01 fleece are in transit. They will be released by customs after 31 Oct
2026, so the definitive duty applies to them.

| Rate | Duty on these shipments |
|---|---|
| 39,8 % | 36,000 x 0.398 = **14,328 euros** |
| 48,1 % | 36,000 x 0.481 = **17,316 euros** |

The wording matters: "duty on shipments arriving soon, to pay or secure, if they are
released for free circulation after the act applies". Never "cash due this week".

## Sum 7: money that comes back

Between 14 May and 30 Oct 2026 the provisional duty applied. Suppose Bergmann had 150,000
euros of L01 fleece released in those five and a half months, and provided the security the
act asks for. (That is separate from the 400,000 euros of last year, which the other sums use.)

Now the definitive act says: keep what the definitive rate allows, release the rest.

| | With the producer confirmed | Without |
|---|---|---|
| Secured under the provisional rate | 150,000 x 45,6 % = 68,400 | 150,000 x 50,0 % = 75,000 |
| Kept under the definitive rate | 150,000 x 39,8 % = 59,700 | 150,000 x 48,1 % = 72,150 |
| **Released back to Bergmann** | **8,700 euros** | **2,850 euros** |

The rule in general: for goods released under the provisional duty, the lower of the two
rates counts. If the definitive rate had been higher, the extra would not be collected.
`[LAW 2016/1036, Art 10(3)]`

## Sum 8: what is not counted

| Situation | In the euro figure? | Shown how |
|---|---|---|
| Registration only (3 Dec 2025 to 13 May 2026) | no | "registered: duty may be collected later" |
| A rate that is not a simple percentage (for example euros per tonne, or a minimum price) | no | shown with the act's quote, sent to a person |
| A measure with an open event (a review, an amendment) | no | a note: "a later document mentions this measure" |
| A line whose scope is still unsure | a proposal: the range starts at 0 | issue C-03 settles how this is shown |

## Sum 9: two duties on one line

One product can carry an anti-dumping duty and an anti-subsidy duty at once, though not
both for the same situation `[LAW 2016/1036, Art 14(1)]`. An invented case `[INVENTED]`,
on a line that is not one of Bergmann's nine: bicycle frames with 20 % anti-dumping and
10 % anti-subsidy duty.

```
an invented line: 200,000 euros x (20 % + 10 %) = 60,000 euros
```

Both are shown separately, each with its own act, and then added. The sum carries a note
for Thomas: check that the two duties are not for the same situation.

## What "at last year's volumes" protects us from

Every figure above assumes Bergmann buys this year what it bought last year. It may buy
more, less, or switch supplier because of this very duty. So the desk says "would cost at
last year's volumes" and never "will cost".

## What each lane takes from this

- **Lane C:** sums 1 to 9 are test cases for the euro engine (issue C-03). The prototype
  has 13 checks already; these add the provisional rule and the declaration rule.
- **Lane B:** the engine needs `rate_category` and `invoice_declaration_required` from the
  ledger, and `invoice_declaration_present` and `in_transit_value_eur` from the importer.
- **Lane A:** every rate in these sums came from the parser. One percentage point wrong there
  is 4,000 euros here.
