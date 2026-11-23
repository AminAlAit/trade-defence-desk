# Worked examples

Ten small stories from Bergmann's year. Each one follows real data through one part of the
desk, and each one looks at the project from a different side.

Read them in order the first time. Later, jump to the one your lane needs.

| # | Example | The side it shows | Mostly for |
|---|---|---|---|
| 01 | [One case, four documents](01_ONE_CASE_FOUR_DOCUMENTS.md) | time: how one duty grows from a notice into a five-year measure, and what the ledger holds on each date | lane B |
| 02 | [Reading the duty table](02_READING_THE_DUTY_TABLE.md) | the raw table as the EU publishes it, and five traps for a simple reader | lane A |
| 03 | [The model and the quote gate](03_THE_MODEL_AND_THE_QUOTE_GATE.md) | what the model answers, and how Python catches a wrong answer | lane A |
| 04 | [Whose name is it?](04_WHOSE_NAME_IS_IT.md) | eight name pairs, a trader, a look-alike, and why spelling alone fails | lane B |
| 05 | [In scope or not?](05_IN_SCOPE_OR_NOT.md) | four fleeces, one act: what a code decides, and what the scope judge is for | lane C |
| 06 | [The euro maths](06_THE_EURO_MATHS.md) | every sum behind the euro figure, including money that comes back | lane C |
| 07 | [A duty that follows the route](07_A_DUTY_THAT_FOLLOWS_THE_ROUTE.md) | goods sent through another country, and why the desk hands this to a person | lanes B, C |
| 08 | [A quiet day, and an act without a table](08_A_QUIET_DAY.md) | an act that does not hit Bergmann, and a measure that outlived its five years | lanes A, B |
| 09 | [Grading the desk](09_GRADING_THE_DESK.md) | how one exam result is counted, with the interval | all |
| 10 | [From a click to the proof](10_FROM_A_CLICK_TO_THE_PROOF.md) | what is saved when Thomas decides, and what the export looks like | lane C |

Two files next to the examples show what our own data looks like:

- [bergmann_purchase_lines.csv](bergmann_purchase_lines.csv): the purchase lines below, in
  the shape the upload expects.
- [sample_label_32026R2393.yaml](sample_label_32026R2393.yaml): what a hand-written answer
  file for one act can look like.

Both are sketches. The real formats are fixed in issues X-04 and X-05.

You met line L01 and its figures at the kickoff. The examples keep that line so the story
stays one story, and then go to places the kickoff did not: earlier dates, other lines,
other acts, and what happens behind the screen.

## What is real and what is invented

- **Real:** every act with a number like 2026/2393, its rates, codes, dates, quotes and
  producer names. The quotes were read from the EU's own text on 2026-11-23. You can check
  them in [data/sample_acts/](../../data/sample_acts/README.md).
- **Invented:** Bergmann, Thomas, the purchase lines below, every euro amount, and anything
  marked `[INVENTED]`. One act in example 07 is invented and says so.
- **Not results:** scores in these examples are illustrations. We have no results yet.

## Bergmann's purchase lines used in the examples `[INVENTED]`

| Line | Goods | Product code | Supplier | Producer on the invoice | Made in | Bought last year |
|---|---|---|---|---|---|---|
| L01 | Root-barrier fleece, polyester, 180 g/m2, 1.2 mm thick, with binder | TARIC 5603 14 80 70 | Hubei Unibon Non-Woven Co., Ltd. | the same | China | 400,000 euros |
| L02 | The same fleece, second source | TARIC 5603 14 80 70 | Ningbo Seaway Trading Co., Ltd. (a trader) | Hebei Saikefu Nonwoven Co Ltd | China | 120,000 euros |
| L03 | Pond underlay fleece, polyester, 300 g/m2, 3 mm thick | CN 5603 14 80, no TARIC code on file | Shandong Luye Geotextile Co., Ltd. | the same | China | 85,000 euros |
| L04 | Frost-protection fleece, 30 g/m2 | CN 5603 12 90 | Shandong Luye Geotextile Co., Ltd. | the same | China | 20,000 euros |
| L05 | Plywood for garden benches | | Curitiba Compensados Ltda | the same | Brazil | 150,000 euros |
| L06 | E-bike motors | | Suzhou Hengli Drive Co Ltd | the same | China | 300,000 euros |
| L07 | Glow-in-the-dark tent pegs, steel | | Binh Phat Metal JSC | the same | Viet Nam (as declared) | 60,000 euros |
| L08 | Solar garden gnomes | | Lucky Gnome Garden Co Ltd | the same | China | 45,000 euros |
| L09 | Geotextile fleece roll, polyester, 200 g/m2 | CN 5603 14 80, no TARIC code on file | Shandong Luye Geotextile Co., Ltd. | the same | China | 30,000 euros |

Two producer names are real, because they come from the real act: Hubei Unibon and Hebei
Saikefu. The spellings on Bergmann's invoices are invented. Bergmann buying from them is
invented. Every purchase, invoice, shipment and decision in these examples is invented.
Nothing here says anything about these companies beyond what the public act says.

## The real case behind most examples

PET spunbond from China. PET spunbond is a strong polyester fleece.

| Date | Document | What it did |
|---|---|---|
| Mon 15 Sep 2025 | Notice C/2025/5010 | the investigation starts |
| Tue 2 Dec 2025 | Regulation (EU) 2025/2409 | customs starts registering the imports |
| Wed 13 May 2026 | Regulation (EU) 2026/1063 | provisional duty |
| Fri 30 Oct 2026 | Regulation (EU) 2026/2393 | definitive duty |
