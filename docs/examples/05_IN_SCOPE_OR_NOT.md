# Example 05: In scope or not?

**The side it shows:** the product. Before any rate matters, one question comes first: is
this purchase line the product the act talks about?

The act is real: Regulation (EU) 2026/2393. Bergmann's four fleeces are `[INVENTED]`, and so
are the scope judge's answers: we have not run a model on these lines yet.

## What the act covers

Article 1(1) describes the product in one long sentence. Cut into its conditions:

| Condition in the act's words | Plain meaning |
|---|---|
| "non-woven needle-punched sheets of polyester filaments" | a polyester fleece |
| "weighing more than 70 g/m2" | not the very light ones |
| "of a thickness exceeding 0,5 mm but not exceeding 1,8 mm" | between half a millimetre and 1.8 mm |
| "impregnated with one or more binders" | soaked with a binder |
| "containing less than 30 % of glass fibres by weight" | mostly polyester |
| "not coated or covered" | no extra layer on top |
| "originating in the People's Republic of China" | made in China |

And the codes: "CN codes ex 5603 13 90, 5603 14 20 and ex 5603 14 80 (TARIC codes
5603 13 90 70 and 5603 14 80 70)".

Read the codes carefully:

- The description in the sentence above is what counts. The codes only say where such
  goods are "currently falling".
- **ex 5603 14 80** has "ex". Only part of this code can be covered: the part with TARIC
  code 5603 14 80 **70**.
- **5603 14 20** has no "ex". The whole code is a candidate. The description still has to fit.

## Four fleeces, four different roads

### L01: the TARIC code decides

Root-barrier fleece, declared under TARIC **5603 14 80 70**, made in China.

The 10-digit code is exactly the one the act names. Python decides alone:

```
product_status: in scope     (reason: TARIC code 5603 14 80 70 is listed; origin China)
```

No model needed. Next stop: name matching.

### L04: the code says no

Frost-protection fleece, CN **5603 12 90**.

The act lists three codes. This is none of them. Python decides alone:

```
product_status: out of scope (reason: code not in the act)
```

On screen this reads "no matching measure found in the acts we read", never "no duty".

### L03: the code cannot decide

Pond underlay fleece. Bergmann's file holds only the 8-digit code **5603 14 80**, and the
act says **ex** 5603 14 80. Only part of that code is covered, and the 8 digits do not say
which part.

```
product_status: unsure       (reason: "ex" code, no TARIC code on the line)
```

Now the scope judge reads Bergmann's description against the act's sentence.

| | |
|---|---|
| Bergmann's description | "Pond underlay fleece, polyester, 300 g/m2, 3 mm thick" |
| The judge's verdict | **outside the act's scope** |
| The judge's quote | "of a thickness exceeding 0,5 mm but not exceeding 1,8 mm" |
| The judge's explanation | "The line states a thickness above the range in the quoted condition." |

Then three things happen:

1. Python checks that the quote is in the act, word for word. It is.
2. The number guard checks the explanation. It contains no digit of its own. It passes.
3. **Thomas confirms.** The judge only proposes. Until he clicks, L03 stays "unsure" and
   its 85,000 euros stay inside the range.

### L09: the judge does not know

Geotextile fleece roll. Again only CN 5603 14 80.

| | |
|---|---|
| Bergmann's description | "Geotextile fleece roll, polyester, 200 g/m2" |
| The judge's verdict | **not sure** |
| The judge's reason | "The description gives no thickness and does not say whether a binder is used." |

This is the answer we want here. The description is too thin to decide. A model that
guessed "in scope" or "outside" would be right half the time and wrong in a way nobody sees.

Thomas gets a task instead: "Ask the supplier for the data sheet of this fleece."

## Why the judge may propose but not decide

| The judge says | The truth | What happens | How bad |
|---|---|---|---|
| in scope | in scope | Thomas sees the duty | fine |
| outside | outside | Thomas confirms, the line drops out | fine |
| in scope | outside | Thomas sees a duty he does not owe, checks, corrects | annoying |
| **outside** | **in scope** | **Thomas believes he is safe and is not** | **the worst case** |
| not sure | either | Thomas gets a task | fine |

The baseline we compare against is the dull one: "never outside the scope". It never makes
the worst mistake, and it never saves Thomas any work. The judge has to do better than
that without making the worst mistake. Issue C-08 counts exactly this.

## Two kinds of "outside"

This act limits its product by description, and has no list of exclusions. Other acts
add an explicit list of products that are excluded. The judge handles both the same way:
one condition, one quote, one verdict.

The original plan described the judge only for explicit exclusions. These examples widen
it to limits in the description, because our main example act has no exclusion list. The
test pairs in issue X-16 need to say which kind each pair is.

A wording rule belongs here. We say a product is **outside the act's scope** or
**excluded from the act's scope**. We never say "exempt". In this area of law "exemption"
means something else.

## What each lane takes from this

- **Lane C:** L01 and L04 are `match_product` (issue C-04). L03 and L09 are the scope judge
  (issue C-07). The table of four outcomes is the scoring sheet for C-08.
- **Lane B:** the synthetic importer needs lines of all four kinds, or the judge is never
  tested.
- **Lane A:** the product sentence and the code list come from the extraction. If the
  model drops the word "ex", L03 would wrongly be "in scope".
