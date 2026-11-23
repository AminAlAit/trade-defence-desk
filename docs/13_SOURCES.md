# 13 Sources, and where to research on your own

## Where our data comes from

| Source | What we take | Does it work? |
|---|---|---|
| **Cellar**, the EU Publications Office's catalogue. Query endpoint: `https://publications.europa.eu/webapi/rdf/sparql`. Its query language is called SPARQL. The query itself is written in issue B-01. | the list of acts and notices, by title and date | yes: answered in 0.29 s; 14 regulations in 30 days, 103 in 12 months, 9 notices in 30 days `[MEASURED 2026-11-13]` |
| **Act text**: `http://publications.europa.eu/resource/celex/{CELEX}` with the headers `Accept: application/xhtml+xml` and `Accept-Language: eng` | the full text of one act | yes: `32026R2393` gave 232,083 bytes `[MEASURED 2026-11-13]`, and again on 2026-11-23 |
| EUR-Lex website | links for people to click | scripts are blocked, so we use it only for human links `[MEASURED 2026-11-13]` |
| TARIC consultation and bulk files | (nothing) | no free structured feed in three attempts `[MEASURED 2026-11-13]`. Not used. |
| List of CN product codes | valid 8-digit codes | exact download source is `[VERIFY]` (issue B-08) |
| OpenSanctions entity pairs | training pairs for the name matcher | free for non-commercial use (CC BY-NC 4.0), 409 MB. **Never commit it to this repository.** Download on demand, and read it as a stream, never whole. |
| German act text (`Accept-Language: deu`) | (later, maybe) | `[VERIFY]` |

Try it yourself. This one line downloads the fleece act:

```
curl -L -H "Accept: application/xhtml+xml" -H "Accept-Language: eng" -o act.xhtml http://publications.europa.eu/resource/celex/32026R2393
```

## Three traps in the act text

All measured on real acts `[MEASURED 2026-11-13]`.

1. **Decimal commas and invisible spaces.** A rate is written "39,8". A code is written
   "ex 5603 14 80", with special non-breaking spaces between the groups.
2. **Grouped cells.** The duty table is built from tables inside tables. A simple row
   reader gives a rate to the wrong company.
3. **Noise, and different kinds of act.** Act 2026/2393 has 196 `<table>` elements. Most
   are just layout for the reasons. A review act such as 2026/2311 has no company table at
   all. So each kind of act needs its own reading.

## How many acts of each kind

The only measured sample is the 14 regulations of the 30 days to 13 Nov 2026:

| Kind | Count |
|---|---|
| provisional duties | 2 |
| definitive duties | 3 (one of them an expiry review with no company table) |
| registrations | 5 |
| repeals | 2 |
| amendments | 2 |

Only about a third of the acts set duties. That is why we download 24 months, about 200
acts `[EST]`. Issue B-03 reports the real counts.

## The four sample acts in this repository

[data/sample_acts/](../data/sample_acts/README.md) holds four real acts: the three
regulations of one case (PET spunbond from China) and one very different act (thermal
paper from Korea). Open them and read Article 1 of each.

## Read the law yourself

Links for people. Open them in a browser:

| Act | Link |
|---|---|
| The fleece act, definitive duty | http://data.europa.eu/eli/reg_impl/2026/2393/oj |
| The same case, provisional duty | http://data.europa.eu/eli/reg_impl/2026/1063/oj |
| The same case, registration | http://data.europa.eu/eli/reg_impl/2025/2409/oj |
| The same case, notice of initiation | http://data.europa.eu/eli/C/2025/5010/oj |
| Thermal paper from Korea, expiry review | http://data.europa.eu/eli/reg_impl/2026/2311/oj |
| The basic anti-dumping regulation | http://data.europa.eu/eli/reg/2016/1036/oj |

The articles of the basic regulation worth reading first: Article 7 (provisional duties),
Article 9 (definitive duties), Article 10 (collecting backwards), Article 11 (how long,
and reviews), Article 13 (circumvention), Article 14 (registration).

## Good places to look around

| Place | What you find |
|---|---|
| https://policy.trade.ec.europa.eu/enforcement-and-protection/trade-defence_en | the Commission's plain explanation of trade defence |
| https://tron.trade.ec.europa.eu/investigations/ongoing | the Commission's list of running investigations, case by case |
| https://trade.ec.europa.eu/access-to-markets/en/home | Access2Markets: duties and rules per product and country, for traders |
| https://ec.europa.eu/taxation_customs/dds2/taric/taric_consultation.jsp?Lang=en | TARIC for people: type a product code and an origin, see the measures |

A good first exercise: look up code `5603 14 80 70` with origin China in the TARIC
consultation, and compare what you see with Article 1 of act 2026/2393.

## Questions worth researching

- What does a customs declaration look like, and where does the TARIC additional code go?
- How does an importer learn about a new act today? (Newsletters of forwarders, chambers
  of commerce, law firms.)
- What is the difference between a producer, an exporter and a trader in these acts?
- How do the UK and the US do the same thing? (The UK Trade Remedies Authority; the US
  Federal Register for anti-dumping orders.)

Write what you find into an issue or bring it to the standup. If it changes a fact in
these docs, change the doc in a pull request.

## Reuse and attribution

Act texts: © European Union, source: Publications Office of the European Union, EUR-Lex.
We expect that EU legal texts may be reused with attribution, under Commission Decision
2011/833/EU. We have not read that decision or the EUR-Lex legal notice ourselves yet, so
this stays `[VERIFY]` until someone on the team has. Only the Official Journal itself is
authentic.

This repository has no licence file yet. Choosing one is a team decision.
