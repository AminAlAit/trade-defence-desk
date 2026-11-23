# Example 04: Whose name is it?

**The side it shows:** names. The rate belongs to a producer. Bergmann's invoice and the
EU's act almost never spell that producer the same way.

Names from the act are real. Names on Bergmann's invoices are `[INVENTED]`.

## What the law says about names

The reasons of Regulation (EU) 2026/2393 are strict (paragraph 155):

> "These duty rates are thus exclusively applicable to imports of the product under
> investigation originating in the country concerned and produced by the named legal
> entities. Imports of the product concerned manufactured by any other company not
> specifically mentioned in the operative part of this regulation, including entities
> related to those specifically mentioned, cannot benefit from these rates"

So "it is the same group" is not enough. It has to be the same legal entity. That is why
our wording rule says "same legal entity", never "same company".

## Step 1: clean both names the same way

Lower case. Remove dots, commas and brackets. Remove legal forms such as "Co", "Ltd",
"JSC", "Joint Stock Company".

| Written | After cleaning |
|---|---|
| Hubei Unibon Non-Woven Co., Ltd. | hubei unibon non-woven |
| Hubei Unibon nonwovens Co Ltd | hubei unibon nonwovens |

## Step 2: score the spelling

A spelling score runs from 0 (nothing in common) to 100 (identical). The scores below
were computed on 2026-11-23 with Python's built-in `difflib` on the cleaned names. Our
baseline will use the `rapidfuzz` library, so the exact numbers will differ a little.

| # | On Bergmann's invoice | In the act | Score | The truth |
|---|---|---|---|---|
| 1 | Shouguang Fada Cloth Company Limited | Shouguang Fada Cloth Co., Ltd. | 100 | same legal entity |
| 2 | Jiangyin Huasicheng Non Woven Co., Ltd | Jiangyin Huasicheng Nonwoven Co., Ltd. | 98.2 | same legal entity |
| 3 | Hebei Saikefu Nonwoven Co Ltd | Hebei Saikefu Nonwovens Co., Ltd. | 97.8 | same legal entity |
| 4 | Hubei Unibon Non-Woven Co., Ltd. | Hubei Unibon nonwovens Co Ltd | 95.5 | same legal entity |
| 5 | Tiandingfeng Nonwovens (Changde) Co., Ltd. | Tiandingfeng Nonwovens Co Ltd | 84.6 | unclear: which of the two names in the row? |
| 6 | Hubei Unibon Non-Woven Co., Ltd. | Hubei Bushi Nonwovens Co., Ltd. | 79.1 | **different companies** |
| 7 | Hubei Unibon New Materials Co., Ltd. `[INVENTED]` | Hubei Unibon nonwovens Co Ltd | 66.7 | **a different legal entity**, even if related |
| 8 | Ningbo Seaway Trading Co., Ltd. | Hebei Saikefu Nonwovens Co., Ltd. | 27.3 | different companies |

The scores use a decimal point, because they are our numbers. Rates keep the comma,
because that is how the act writes them.

## What a single threshold does with this

A threshold is a cut-off: above it, the system says "same".

Suppose the baseline says "same" above 75.

- Pairs 1 to 5: accepted. Fine so far.
- **Pair 6: accepted, and wrong.** Unibon and Bushi are two producers in the same province
  with the same last word. Unibon has 39,8 %. Bushi is in the annex with 47,1 %. The
  spelling is close. The companies are not.

Suppose we raise the threshold to 90 to be safe.

- Pair 6 is now rejected. Good.
- Pair 5 is rejected too. It then gets the fallback rate. In this act that costs nothing,
  because both are 48,1 %. In another act it would.

No single number separates right from wrong here. That is the reason for the trained model.

## What the trained model adds

It does not look at one score. It looks at several signals for each pair, for example:

- the spelling score of the whole cleaned name;
- whether the **distinctive word** matches ("unibon" against "bushi");
- whether the place name matches;
- whether only the legal form or a plural "s" differs;
- how long the names are.

It learns from many pairs that people have already judged, and gives back a probability
between 0 and 1. Whether it really beats the plain score is what issue B-11 measures, on
about 300 test pairs labelled by the other two lanes.

## Tiers: what happens with the result

The matcher sorts every pair into one of four tiers. The names and the cut-offs below are
a working proposal `[INVENTED]`; issue B-10 fixes them. In the real system the tiers come
from the model's probability. Here the spelling score stands in for it.

| Tier | Rule in this sketch | What the desk does | Pairs from the table |
|---|---|---|---|
| 1 identical | the same after cleaning | accepts, shows it | 1 |
| 2 very likely | score of 97 or more | accepts, shows it | 2, 3 |
| 3 uncertain | score from 75 to below 97 | **asks Thomas** | 4, 5, 6 |
| 4 no match | below 75 | the line falls to the fallback rate, and says so | 7, 8 |

Pair 4 is the question from the kickoff: "Is the producer on your invoice the same legal
entity as the one in the act?" At 95.5 it sits just below the cut-off, so the desk asks.
That is the right call here: 33,200 euros hang on the answer (see example 06).

Pair 7 lands in tier 4, and that deserves a second look. The name on the invoice shares
"Hubei Unibon" with a listed producer. A good desk says so: "no match, but one name in the
act looks related". The law says related entities do not get the rate.

## The safe threshold is chosen, not guessed

- Above it, the matcher decides alone.
- We set it on a separate validation set, so that almost nothing wrong gets through.
- Then we report two numbers together: how often the matcher is right when it decides
  alone, and what share of pairs it hands to a person.

A matcher that asks about everything is always right and useless. A matcher that never
asks is fast and dangerous. The pair of numbers shows the trade.

## The trader

Line L02: Bergmann buys from **Ningbo Seaway Trading Co., Ltd.**, a trader. The trader is
in no act (pair 8). If the desk matched suppliers, it would say "no match" and give L02 the
fallback rate.

But the invoice names the producer: **Hebei Saikefu Nonwoven Co Ltd**. That is pair 3, and
it is in the annex with 47,1 %.

So the desk matches `producer_name` first, and the supplier only when no producer is named.

## The error that hurts most

| Error | What happens | How bad |
|---|---|---|
| A true match is missed | the line silently gets the fallback rate; Thomas overestimates | costly, but on the safe side |
| A false match is accepted | the line gets a low rate it has no right to; Thomas underestimates and is surprised at the border | the worst case |

So when in doubt, the matcher asks.

## What each lane takes from this

- **Lane B:** pairs 4, 6 and 7 are the kinds of pair the test set must contain: a true
  variant, a look-alike in the same place, and a related name.
- **Lane A:** every name of a grouped cell must reach the ledger as its own alias,
  otherwise pair 5 has nothing to match against.
- **Lane C:** tier 3 becomes a question on the decisions list, with both spellings side by
  side.
