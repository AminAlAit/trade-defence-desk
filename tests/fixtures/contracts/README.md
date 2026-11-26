# Contract examples

One file per contract, so each lane can build before the real producer exists.

- `sections_*` and `extraction_*_parser.json`: real. Made by the normaliser and the parser
  from `data/sample_acts/`.
- `extraction_*_llm_example.json`: the quotes are real, from the act. No model ran. The
  values were picked by hand to show the shape.
- `field_checks_*`: the shape of three verdicts. The third is the 2026/1036 slip from
  `docs/examples/03_THE_MODEL_AND_THE_QUOTE_GATE.md`.
- Bergmann's suppliers, scope judgements, decisions, log and runs: `[INVENTED]`,
  taken from `docs/examples/05` and `docs/examples/10`.
- Bergmann's purchase lines: `docs/examples/bergmann_purchase_lines.csv`, the CSV format itself.
