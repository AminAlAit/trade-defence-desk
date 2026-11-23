# Example 09: Grading the desk

**The side it shows:** honesty. How one exam result is counted, and how much a small exam
can really prove.

**Every score here is `[INVENTED]`.** We have no results yet. Do not quote these numbers
as ours.

## What "correct" means for one act

Take the fleece act. The hand-written answer has 8 rows (see example 02). The system's
answer is compared row by row: name or names, rate and code together.

| Code | Hand-written answer | System | Row correct? |
|---|---|---|---|
| 88CB | Hubei Unibon nonwovens Co Ltd, 39.8 | the same | yes |
| 88CC | two names, 48.1 | **one name**, 48.1 | **no** |
| 88CD to 88CH | five rows, 47.1 | the same | yes |
| 8999 | all other imports, 48.1 | the same | yes |

Seven rows of eight are right. **The act still counts as wrong.**

That is strict on purpose. Thomas does not use seven eighths of a table. If the one wrong
row is his supplier, the whole case is wrong for him.

## The exam, counted

Suppose the sealed exam has 25 acts, and 12 of them have a company table. The main number
is counted on those 12.

### Parser only

It accepts everything it reads.

- 10 of 12 acts fully correct.

### Model only

- 8 of 12 acts fully correct.

### Combined

The combined system takes the parser's rows and lets the model and the verifier check
them. It may say "I am not sure, a person should look".

- It sends 3 of the 12 acts to a person.
- It accepts 9 on its own.
- All 9 are fully correct.

| System | Correct among accepted | Coverage |
|---|---|---|
| Parser only | 10 of 12 | 12 of 12 = 100 % |
| Model only | 8 of 12 | 12 of 12 = 100 % |
| Combined | 9 of 9 | 9 of 12 = 75 % |

**Coverage** is the share the system handled alone. Without it, the combined number would
be a trick: a system that sends everything to a person is never wrong.

## How sure are we? The interval

9 of 9 looks perfect. But 9 acts are few. If the true quality were only 80 %, getting
9 right in a row would still happen about one time in seven.

A 95 % interval says: given what we saw, the true value plausibly lies in this range. We
use the Wilson method. For a perfect score we use the stricter exact method
(Clopper-Pearson), as [10_EVALUATION.md](../10_EVALUATION.md) says.

| System | Result | 95 % interval |
|---|---|---|
| Parser only | 10 of 12 = 83 % | 55 % to 95 % |
| Model only | 8 of 12 = 67 % | 39 % to 86 % |
| Combined | 9 of 9 = 100 % | 66 % to 100 % |

Read the last row slowly. A perfect score on 9 acts only shows that the true value is
probably above 66 %.

And with the whole exam? Even 25 of 25 gives an interval from 86 % to 100 %. Our bar is
90 %. So even a perfect exam does not prove we are above the bar. We say that in the
README, in those words.

If you want to check the sums, the lower end for a perfect score on n acts is the n-th
root of 0.025:

```
n = 9:    0.025 ^ (1/9)  = 0.66
n = 25:   0.025 ^ (1/25) = 0.86
```

And the "one time in seven" above: 0.8 multiplied by itself 9 times is 0.13.

## Which system is better?

The intervals of the three systems overlap a lot. So we do not say "the combined system is
better" from the table alone.

All three systems ran on the same 12 acts. So we look at what the safety net did with each
act:

| | Count |
|---|---|
| the parser was right, and the combined system accepted the act | 9 |
| the parser was wrong, and the combined system sent the act to a person | 2 |
| the parser was right, and the combined system still sent the act to a person | 1 |
| the parser was wrong, and the combined system accepted the act | 0 |

This table is the real finding. The safety net caught both of the parser's mistakes. It
raised one false alarm, which costs a person a few minutes. It let no mistake through. A
statistical test on such small counts is reported too, with the honest remark that it
cannot show much.

## How the sentence in the README would read

> Sealed exam, 25 acts, 12 with company tables, labelled blind, run once.
> Combined system: 9 of 9 accepted tables fully correct (95 % interval 66 to 100 %),
> at 75 % coverage. Parser only: 10 of 12 (55 to 95 %). Model only: 8 of 12 (39 to 86 %).

Notice what it does not say: "100 % accurate".

## What could go wrong with the grading itself

| Mistake | What it does | Our guard |
|---|---|---|
| Tuning on the exam acts | the scores look great and mean nothing | the exam is sealed and run once |
| A provisional act in practice, its definitive act in the exam | the system has seen the same companies and layout | whole cases go to one side |
| Picking the best-looking number after the run | every project looks good on some number | the written promise, before the run |
| An act that crashes the parser is left out | the score goes up | a crash counts as wrong |
| The person who built it also wrote the answers | blind spots are shared | nobody grades their own homework |
| The hand-written answers are wrong | we measure against a wrong ruler | 5 exam acts are labelled twice and compared |

## What each lane takes from this

- **Lane A:** the counting above is the evaluation harness (issue A-06). The interval
  function gets a test with exactly these numbers.
- **Lanes B and C:** you write the answers the system is graded on. One sloppy label moves
  the main number by 8 points when n is 12.
- **All:** on Fridays, show your number with its n and its interval. Always.
