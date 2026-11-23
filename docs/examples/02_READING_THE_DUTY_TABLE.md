# Example 02: Reading the duty table

**The side it shows:** the raw material. What the EU really publishes, and why "just read
the table" is a week of work for lane A.

The act is real: Regulation (EU) 2026/2393, read on 2026-11-23. Only the "model says"
column near the end is `[INVENTED]`: we have not run a model on this act yet.

## What a person sees

| Company | Definitive anti-dumping duty (%) | TARIC additional code |
|---|---|---|
| Hubei Unibon nonwovens Co Ltd | 39,8 | 88CB |
| Changde Tiandingfeng Nonwovens Co Ltd, Tiandingfeng Nonwovens Co Ltd | 48,1 | 88CC |
| Other cooperating companies | 47,1 | See Annex |
| All other imports originating in the People's Republic of China | 48,1 | 8999 |

Four rows. Easy.

## What the file really contains

The same table in the downloaded file, with the styling removed and shortened:

```html
<tr>
  <td>
    <table><tr><td>(dash)</td><td>Hubei Unibon nonwovens Co Ltd</td></tr></table>
  </td>
  <td>39,8 </td>
  <td>88CB</td>
</tr>
<tr>
  <td>
    <table><tr><td>(dash)</td><td>Changde Tiandingfeng Nonwovens Co Ltd</td></tr></table>
    <table><tr><td>(dash)</td><td>Tiandingfeng Nonwovens Co Ltd</td></tr></table>
  </td>
  <td>48,1 </td>
  <td>88CC</td>
</tr>
<tr>
  <td>Other cooperating companies</td>
  <td>47,1 </td>
  <td>See Annex</td>
</tr>
```

Each company name sits in its own small table **inside** the first cell. The second row
has two small tables in one cell. That is the grouped cell.

## Five traps, all in this one act

### Trap 1: tables inside tables

A simple reader that walks over every `<tr>` in the document finds the inner rows too.
It sees a "row" that holds only a dash and "Tiandingfeng Nonwovens Co Ltd", with no rate
and no code. Depending on how it repairs that, it drops the company or gives it the
neighbour's rate.

The right reading: one outer row, two names, one rate, one code.

### Trap 2: four tables list the same companies

The act holds four tables with these company names:

| Where | What its numbers are | For Hubei Unibon |
|---|---|---|
| in the reasons | the dumping margin | 39,8 |
| in the reasons | the underselling margin | **57,5** |
| in the reasons | the duty, without codes | 39,8 |
| **Article 1(2)** | **the duty, with codes** | **39,8** |

Only the last one is law. The second one is the real trap: same companies, same layout,
different numbers. A parser that takes "the first table with company names and
percentages" can come back with 57,5 %. So the parser must know which part of the act a
table sits in, and take the one from the operative part.

### Trap 3: 196 tables

The file has 196 `<table>` elements. Almost all are layout: every numbered paragraph of
the reasons is a one-row table with the number in the left cell. The parser has to find
the two or three tables that matter.

### Trap 4: the comma and the spaces

- The rate is "39,8", with a comma and a trailing space. As a number it is 39.8.
- Product codes are written in groups, "5603 14 80", sometimes with special non-breaking
  spaces that look normal on screen but are a different character.
- We keep the text exactly as written, and convert a copy for calculating.

### Trap 5: "See Annex"

The third row has no code. Its code column says "See Annex". The annex at the end lists
five producers, each with its own code:

| Name in the annex | Code |
|---|---|
| Hebei Jinliu Chemical Fiber Co., Ltd. | 88CD |
| Hebei Saikefu Nonwovens Co., Ltd. | 88CE |
| Hubei Bushi Nonwovens Co., Ltd. | 88CF |
| Shouguang Fada Cloth Co., Ltd. | 88CG |
| Jiangyin Huasicheng Nonwoven Co., Ltd. | 88CH |

So one row of the table becomes five rows in our database, all at 47,1 %.

Look at the spelling too: the main table writes "Co Ltd", the annex writes "Co., Ltd.".
Same act, two styles. Lane B's name matcher has to live with that.

## What the parser should give back

Our ledger keeps one row per code. So the four visible rows become eight:

```json
[
  {"code": "88CB", "category": "individual", "rate_pct": 39.8,
   "names": ["Hubei Unibon nonwovens Co Ltd"]},
  {"code": "88CC", "category": "individual", "rate_pct": 48.1,
   "names": ["Changde Tiandingfeng Nonwovens Co Ltd", "Tiandingfeng Nonwovens Co Ltd"]},
  {"code": "88CD", "category": "cooperating_not_sampled", "rate_pct": 47.1,
   "names": ["Hebei Jinliu Chemical Fiber Co., Ltd."]},
  {"code": "88CE", "category": "cooperating_not_sampled", "rate_pct": 47.1,
   "names": ["Hebei Saikefu Nonwovens Co., Ltd."]},
  {"code": "88CF", "category": "cooperating_not_sampled", "rate_pct": 47.1,
   "names": ["Hubei Bushi Nonwovens Co., Ltd."]},
  {"code": "88CG", "category": "cooperating_not_sampled", "rate_pct": 47.1,
   "names": ["Shouguang Fada Cloth Co., Ltd."]},
  {"code": "88CH", "category": "cooperating_not_sampled", "rate_pct": 47.1,
   "names": ["Jiangyin Huasicheng Nonwoven Co., Ltd."]},
  {"code": "8999", "category": "residual", "rate_pct": 48.1,
   "names": []}
]
```

In the database, each of these is one `measure_rate` row, and each name is one
`company_alias` row.

## Why a model reads it a second time

The model gets the same Article 1 and annex and returns its own list of rows. Then Python
compares the two lists, code by code.

| Code | Parser says | Model says | Result |
|---|---|---|---|
| 88CB | 39.8, one name | 39.8, one name | agree: accepted |
| 88CC | 48.1, two names | 48.1, two names | agree: accepted |
| 88CE | 47.1 | 47.1 | agree: accepted |
| 8999 | 48.1 | 48.1 | agree: accepted |

When they disagree on any row, the act goes to a person. Neither side wins silently. If
the parser had fallen into trap 1, the model would very likely not have made the same
mistake, and the difference would have raised a flag.

## Try it yourself

1. Download the act with the `curl` line in [13_SOURCES.md](../13_SOURCES.md), or unpack it
   from [data/sample_acts/](../../data/sample_acts/README.md).
2. Search the file for `88CC`.
3. Look at what stands in the cell to the left of it.

## What each lane takes from this

- **Lane A:** this act is the pinned test of the parser (issue A-02). The expected output
  above is the test.
- **Lane B:** `company_alias` exists because of the grouped cell. Two names, one `rate_id`.
- **Lane C:** the case page shows "company rows by kind". The three kinds come from the
  `category` field above.
