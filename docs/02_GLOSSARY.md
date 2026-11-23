# 02 Glossary

Plain meanings first. Each entry ends with one example from Bergmann's world.
Words in the database are written like `this`.

## The basics

| Word | Plain meaning | Example |
|---|---|---|
| Customs | The state office that checks goods at the border and collects duties. | Bergmann's fleece arrives in Hamburg and is declared to customs there. |
| Importer | A company that buys goods outside the EU and brings them in. | Bergmann Outdoor GmbH. |
| Duty | Money the importer pays to customs when goods enter the EU. Never call it a tax. | A share of the price of each shipment of fleece. |
| Customs value | The price the duty is calculated on. The acts call it the "net, free-at-Union-frontier price, before duty". | Bergmann's fleece purchases were worth 400,000 euros last year `[INVENTED]`. |
| Release for free circulation | The moment customs lets the goods into the EU market. The duty applies at this moment. | A container that is still in port has not been released yet. |
| Official Journal (OJ) | The EU's daily legal newspaper. An act counts only once it is published there. | Regulation 2026/2393 was published on Fri 30 Oct 2026. |

## Trade defence

| Word | Plain meaning | Example |
|---|---|---|
| Trade defence | The EU's tools against unfairly cheap imports. | Anti-dumping duties, anti-subsidy duties, safeguards. |
| Dumping | Selling a product abroad for less than at home. | A producer sells fleece to the EU below its home price. |
| Anti-dumping duty (AD) | An extra duty that makes up for dumping. | 39,8 % for one Chinese fleece producer. |
| Anti-subsidy duty, countervailing duty (CVD) | An extra duty that makes up for state subsidies to the producer. | Can sit on top of an anti-dumping duty on the same product. |
| Safeguard | A measure against a sudden flood of imports from all countries. Out of our scope. | The desk shows it and does not apply it. |
| Investigation | The Commission's check whether dumping happens and harms EU producers. It takes about a year. | The fleece case started on 15 Sep 2025. |
| Notice of initiation | A short public note that an investigation or a review starts. No duty yet. | Notice C/2025/5010. |
| Measure | One duty on one product from one country, with its rates and dates. Our ledger has one card per measure. | "Anti-dumping, PET spunbond, China". |

## The act

| Word | Plain meaning | Example |
|---|---|---|
| Act | One legal text published in the Official Journal. | Regulation (EU) 2026/2393. |
| Regulation | The kind of act that sets duties. It applies in all EU countries directly. | "Commission Implementing Regulation (EU) 2026/2393". |
| CELEX number | The EU's id for an act. `3` + year + `R` + number means a regulation. | `32026R2393`. |
| Recitals | The long first part of an act that explains the reasons. No rules in it. | 2026/2393 has 170 numbered paragraphs of reasons. |
| Operative part | The short part with the rules. It starts after "HAS ADOPTED THIS REGULATION". | Articles 1 to 4 of 2026/2393. |
| Article | One numbered rule in the operative part. | Article 1 sets the duty and holds the duty table. |
| Annex | An attachment at the end of the act, often a list of companies. | The annex of 2026/2393 lists five more producers. |
| Duty table | The table of companies, rates and codes in Article 1. | Four rows in 2026/2393. |
| Corrigendum | A published correction of a mistake in an act. | The desk shows it and sends it to a person. |

## The stages of a measure

| Word | Plain meaning | Example |
|---|---|---|
| Registration | Customs starts counting the imports. No duty yet, but one may be collected later for these goods. | 2025/2409, from 3 Dec 2025. |
| Provisional duty | A first duty during the investigation. The importer does not pay it for good: the amount is secured with a guarantee. | 2026/1063, from 14 May 2026. |
| Definitive duty | The duty after the investigation ends. It normally runs for five years. | 2026/2393, from 31 Oct 2026. |
| Secured amount | Money or a guarantee set aside for a provisional duty. | Later the definitive act says how much of it is kept. |
| Expiry review | A check, near the end of the five years, whether the duty should continue. The duty stays in force while it runs. | Thermal paper from Korea, 2026/2311. |
| Repeal | An act that ends a measure. | The ledger closes the card on the stated date. |
| Amendment | An act that changes an older act, for example adds a company. | Shown and sent to a person, not applied automatically. |
| Extension | A measure is stretched to goods sent from another country, to stop detours. | See example 07. |
| Circumvention | Getting around a duty, for example by shipping through a third country. | An anti-circumvention investigation looks into it. |
| Undertaking | A producer promises a minimum price instead of paying the duty. | Out of our scope: shown, not applied. |

## The rows of the duty table

| Word | Plain meaning | Example |
|---|---|---|
| Producer | The factory that made the goods. The rate follows the producer, not the seller. | Hubei Unibon nonwovens Co Ltd. |
| Supplier | The company Bergmann buys from. It can be a trader that is not the producer. | A trading house in Ningbo `[INVENTED]`. |
| Company row | One line of the duty table: name or names, rate, code. | "Hubei Unibon nonwovens Co Ltd, 39,8 %, 88CB". |
| Kind of row | The fleece act has the three kinds below. Other acts have other kinds, for example one single rate for a whole country. In the database: `rate_category`. | |
| Individual rate | A rate for one named producer or one group of producers. | 39,8 % for Hubei Unibon. |
| Sample | The Commission cannot examine every producer. It picks a few, the sample, and examines those one by one. | Hubei Unibon was in the sample. |
| Other cooperating companies | One shared rate for producers that helped the investigation but were not in the sample. They are listed in the annex. | 47,1 % for five producers. |
| All other imports | The fallback rate for everyone not named. | 48,1 %, code 8999. |
| Grouped cell | Two or more company names that share one rate and one code in the table. A trap for parsers. | Two "Tiandingfeng" names share 48,1 % and 88CC. |
| Invoice declaration | A signed sentence on the invoice that names the producer. Without it the company rate does not apply. | Worded in Article 1(3) of each act. |
| Same legal entity | The producer on the invoice and the name in the act are one and the same registered company. A person confirms this. | "Hubei Unibon Non-Woven Co., Ltd." and "Hubei Unibon nonwovens Co Ltd". |

## Codes

Three codes, built up on one example:

| What Bergmann writes | Length | It says |
|---|---|---|
| `5603 14 80` | 8 digits, the CN code | what kind of goods: a polyester fleece above 150 g/m2 |
| `5603 14 80 70` | 10 digits, the TARIC code | exactly the part of that code the measure covers |
| `88CB` | 4 characters, the TARIC additional code | whose goods: the row of Hubei Unibon |


| Word | Plain meaning | Example |
|---|---|---|
| Product code | A number that says what kind of goods something is. | Below. |
| CN code | The EU's 8-digit product code (Combined Nomenclature). | `5603 14 80`. |
| "ex" code | "ex" before a code means: only part of the goods under this code are covered. | `ex 5603 14 80`. |
| TARIC code | A 10-digit product code. The two extra digits pick out the exact goods a measure covers. | `5603 14 80 70`. |
| TARIC additional code | A 4-character code for one company row. The importer writes it in the customs declaration to claim that row's rate. | `88CB` for Hubei Unibon. |
| TARIC (the database) | The EU's database of all measures per product code. We cannot read it by machine, so we never claim to check against it. | |
| Origin | The country where the goods were made. Duties normally follow the origin. | China. |
| Country of consignment or dispatch | The country the goods were sent from. It matters for an extended measure. | Goods made in China, shipped from Viet Nam. |

## Bergmann's side

| Word | Plain meaning | Example |
|---|---|---|
| Purchase line | One product from one supplier that Bergmann buys again and again. | "Root-barrier fleece from Hubei Unibon". |
| Last year's volumes | What Bergmann bought on a line in the last full year. The euro figure uses it. | 400,000 euros of fleece `[INVENTED]`. |
| Exposure | The extra duty a measure would cost on a line, at last year's volumes. | 159,200 to 192,400 euros. |
| In transit | Goods already shipped but not yet released by customs. | Two containers at sea. |
| Synthetic importer | A made-up importer with made-up purchases. We never use real customer data. | Bergmann. |

## Our own words

| Word | Plain meaning |
|---|---|
| The desk | Our product. |
| Case | Everything about one measure and one importer: the six questions answered. |
| Ledger | Our database of measures, with their rates, dates and states. |
| Triage | Deciding what kind of act this is, from its title. |
| Extraction | Turning the text of an act into structured facts. |
| Parser | Python code that reads the duty table. No model involved. |
| Quote gate | The check that every fact from the model comes with a word-for-word quote from the act, and that the quote contains the fact. |
| Verifier | The code that runs the quote gate and the other checks, and gives every field a status. |
| Name matcher | The trained model that scores whether two producer names mean the same legal entity. |
| Scope judge | The language model that says whether a product is outside an act's scope, with a quote, or says "not sure". |
| Number guard | A test that fails if the model wrote a digit outside a quote. |
| Decision | Something only a person can settle, saved with a reason. |
| Audit log | The list of all decisions and events, in order. |
| Replay | Playing back stored pipeline runs, sped up, marked "replay" on screen. |
| Practice set | 40 acts with hand-written correct answers. We build and tune on these. |
| Sealed exam | 25 acts locked away. The desk is run on them once. Engineers call this a holdout. |
| Lane | One of three areas of work: A, B or C. |
| Inbox | The first screen: new cases for this importer. |
| Case page | The screen of one case, with the six questions. |
| Green, amber | Green: a fact passed its check. Amber: nobody has confirmed it yet. |
| Ingest | Find and download the acts. |
| Normalise | Cut an act into clean, numbered parts. |
| Euro engine | The code that computes the euro figure. |

## People and offices

| Word | Plain meaning |
|---|---|
| The Commission | The EU body that runs the investigations and writes the acts. |
| The Union | The EU. The acts say "Union". |
| Exporter | The company that sells the goods into the EU. Often the producer, sometimes a trader. |
| Freight forwarder | A company that organises the transport. |
| Customs broker | A company that handles the customs paperwork for an importer. |
| Declarant | Whoever hands in the customs declaration. |
| Union Customs Code (UCC) | The EU's general customs law. It says who owes a duty. We have not read it yet. |
| Incoterm | A standard three-letter term in a sales contract that says who pays for transport and insurance. FOB means: the price covers the goods up to the ship. |

## Project and tech words

| Word | Plain meaning |
|---|---|
| Fixture | A small, fixed example file that tests use. |
| Contract | A data shape that two lanes agree on. |
| SPARQL | The query language of the EU's catalogue. It plays the role SQL plays for a database. |
| YAML | A simple text format for structured data. Our hand-written answers are YAML files. |
| ELI | A stable web address for an EU act. |
| Fingerprint, SHA-256 | A short code computed from a file. If the file changes, the code changes. |
| Token | The unit a language model counts text in. Roughly three quarters of a word. |
| Trace | The record of one model call: what went in, what came out, cost and time. |
| Baseline | The simple method a model must beat to be worth having. |
| Threshold | The score above which the system decides alone. |
| Coverage | The share of cases the system handled without a person. |
| n | How many cases a number is based on. |
| Interval | The range in which the true value plausibly lies, given how few cases we tested. |
| Written promise | What we commit to before the exam: how we will score. Engineers say pre-registration. |
| Freeze tag | A label on one exact version of the code. Ours is called `holdout-freeze`. |
| Walking skeleton | The thinnest version that runs from start to end. |
| Feature freeze | The day after which we only fix, test and document. |
| Retro | A short look back: keep, change, try. |
