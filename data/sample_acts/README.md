# Sample acts

Four real acts, exactly as the EU Publications Office served them on 2026-11-23.
They are here so you can open a real act before any code exists.

| File | Act | What it is | Size unpacked | Published |
|---|---|---|---|---|
| `32025R2409.xhtml.gz` | Regulation (EU) 2025/2409 | registration, PET spunbond from China | 15,388 bytes | Tue 2 Dec 2025 |
| `32026R1063.xhtml.gz` | Regulation (EU) 2026/1063 | provisional duty, same case | 589,001 bytes | Wed 13 May 2026 |
| `32026R2393.xhtml.gz` | Regulation (EU) 2026/2393 | definitive duty, same case | 232,083 bytes | Fri 30 Oct 2026 |
| `32026R2311.xhtml.gz` | Regulation (EU) 2026/2311 | definitive duty after an expiry review, thermal paper from Korea, no company table | 251,757 bytes | Tue 20 Oct 2026 |

The first three are one case at three stages. The fourth is the opposite kind of act.
Both 2026/2393 and 2026/2311 are our fixed example acts and always belong to the practice set.

## How to open one

```
gzip -dk 32026R2393.xhtml.gz
```

Then open `32026R2393.xhtml` in a browser. To find the rules quickly, search the page for
"HAS ADOPTED THIS REGULATION". Everything before it is reasons. Everything after it is law.

## Fingerprints

SHA-256 of the unpacked files. If your download of the same act has a different
fingerprint, the EU has changed the file, and that is worth telling the team.

| File | SHA-256 |
|---|---|
| `32025R2409.xhtml` | `e0f0c4011f1455993ad4a430ea0a480bf4a81d3642c87c957bb4272855b27586` |
| `32026R1063.xhtml` | `a90093429ccf9350e5d81ccabefdd8b5452281afecf7b11a34b83deff6a0f777` |
| `32026R2393.xhtml` | `4ad071c2ee03262acbd24ef42f3046de3669e5b15e96e7c85b5263f929fd92f3` |
| `32026R2311.xhtml` | `3d11a229e6e09be7c698bfb90a2faef143c39368e517288540bd301f84727970` |

## Where they come from

```
curl -L -H "Accept: application/xhtml+xml" -H "Accept-Language: eng" -o 32026R2393.xhtml http://publications.europa.eu/resource/celex/32026R2393
```

© European Union. Source: Publications Office of the European Union. Only the Official
Journal of the European Union is authentic.

## Which examples use which act

| Act | Examples |
|---|---|
| 2025/2409, 2026/1063, 2026/2393 | [01](../../docs/examples/01_ONE_CASE_FOUR_DOCUMENTS.md), [06](../../docs/examples/06_THE_EURO_MATHS.md) |
| 2026/2393 | [02](../../docs/examples/02_READING_THE_DUTY_TABLE.md), [03](../../docs/examples/03_THE_MODEL_AND_THE_QUOTE_GATE.md), [04](../../docs/examples/04_WHOSE_NAME_IS_IT.md), [05](../../docs/examples/05_IN_SCOPE_OR_NOT.md), [10](../../docs/examples/10_FROM_A_CLICK_TO_THE_PROOF.md) |
| 2026/2311 | [08](../../docs/examples/08_A_QUIET_DAY.md) |
