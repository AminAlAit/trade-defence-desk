# Example 07: A duty that follows the route

**The side it shows:** the limits of the desk. Some cases are too tricky to automate in
four weeks. The desk must recognise them and hand them to a person, clearly.

**Everything in this example is `[INVENTED]`**, including the act. It is here to teach
one idea. The legal mechanism behind it is real: Article 13 of the basic anti-dumping
regulation (EU) 2016/1036.

## The background

Normally a duty follows the **origin**: where the goods were made. Fleece made in China
carries the duty, wherever the ship started.

That leaves a detour. A producer under a duty could send its goods to a neighbouring
country, do little or nothing to them there, and ship them to the EU from there, declared
as made in that country. The law calls this circumvention.

The EU's answer is an **extension**: the existing duty is stretched to goods **sent from**
the other country, "whether declared as originating in" that country or not. Honest
producers in that country can apply to be left out, and are then named in the act.

## The invented case

- An existing measure `[INVENTED]`: anti-dumping duty on steel tent pegs from China,
  all other imports 30 %.
- A new act `[INVENTED]`, "Regulation (EU) 2026/9901": the measure is extended to steel
  tent pegs consigned from Viet Nam, whether declared as originating in Viet Nam or not.
- The act names two Vietnamese producers that are left out, because they showed they make
  their pegs themselves.

Bergmann's line L07: glow-in-the-dark tent pegs, steel, bought from **Binh Phat Metal
JSC**, shipped from Hai Phong, declared as made in Viet Nam. 60,000 euros last year.

## What goes wrong if the desk treats this like a normal act

The normal product test asks: is the origin of the line one of the origins of the measure?

```
measure origin: China
line origin:    Viet Nam
result:         out of scope      <- wrong
```

The desk would tell Thomas "no matching measure found", on exactly the act that was
written for goods like his.

## What the ledger holds instead

```
measure #20 (the original)
  origin_countries     China
  liability_basis      origin

measure #21 (the extension)
  extends_measure_id   #20
  origin_countries     Viet Nam (for an extension: the country the goods are sent from)
  liability_basis      consignment
  needs_review         true
```

The flag `liability_basis = consignment` changes the road the line takes:

| Step | Normal measure | Extended measure |
|---|---|---|
| Product code | compared | compared |
| Country test | origin of the line | country of dispatch of the line |
| Result for L07 | out of scope | **sent to a person** |
| Euro figure | computed | not computed; a note instead |

## What Thomas sees

> **Needs your review.** This act extends an existing duty to goods sent from Viet Nam.
> Your line L07 is sent from Viet Nam. The desk does not decide extended measures.
>
> Check: is your producer one of the companies the act leaves out?
> Producer on your invoice: Binh Phat Metal JSC.

With the sentence of the act next to it, and a link to the full text.

It does **not** say "30 % applies", and it does **not** say "you are not affected". Both
could be wrong, and both would be believed.

## Why we do not automate this

To decide this case properly the desk would need to:

1. read the list of producers that are left out, with their own codes;
2. match Bergmann's producer against it;
3. know whether the producer's status is still valid, since these lists change;
4. know where the goods were really made, which the desk cannot know.

Points 1 and 2 are doable later. The tables `exempted_company` and `undertaking` already
exist in the schema for that day, and stay empty for now. Point 4 can never be automated:
the desk does not decide where goods come from.

Building the tables now costs an hour. Changing the schema in week 3 would cost days.

## A wording trap

Suppose a different line: tent pegs made in and shipped from Taiwan, and no act mentions
Taiwan.

| Wrong | Right |
|---|---|
| "Taiwan has no duty." | "This act lists China as origin. We found no duty in it for goods made in Taiwan. Check the ledger for an extension to imports from Taiwan." |

The desk only knows the acts it has read. It says what it found, not what is true in the
world.

## What each lane takes from this

- **Lane B:** `liability_basis`, `extends_measure_id` and `needs_review` are part of the
  ledger from day one (issues B-06, B-07). An extension gets a test with a real act from
  the backfill.
- **Lane C:** `match_product` needs `country_of_dispatch` on every purchase line (issue
  C-04). The review message above is a template, not model text.
- **Lane A:** "extends which measure" is one more field for the extraction, with a quote.
