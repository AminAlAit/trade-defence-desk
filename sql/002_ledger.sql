-- Group 2 of docs/05_DATA_SCHEMA.md: the ledger. Lane B owns these tables. Columns follow
-- Suma's contracts/lane_b.py. For M1 the parser fills them for 2026/2393; B-06 takes over.

CREATE TABLE IF NOT EXISTS measure (
    measure_id          text PRIMARY KEY,
    kind                text NOT NULL,
    stage               text NOT NULL,
    product_text        text NOT NULL,
    origin_countries    text[] NOT NULL,
    liability_basis     text NOT NULL DEFAULT 'origin',
    extends_measure_id  text,
    legal_act_celex     text NOT NULL REFERENCES act (celex),
    valid_from          date,
    valid_from_basis    text,
    valid_to            date,
    valid_to_basis      text NOT NULL DEFAULT 'unknown',
    status              text NOT NULL,
    superseded_by       text,
    has_open_event      boolean NOT NULL DEFAULT false,
    needs_review        boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS measure_rate (
    rate_id                text PRIMARY KEY,
    measure_id             text NOT NULL REFERENCES measure (measure_id),
    origin_country         text NOT NULL,
    taric_additional_code  text,
    rate_category          text NOT NULL,
    rate_pct               numeric(5, 2),
    amount                 numeric,
    unit                   text,
    currency               text,
    formula_text           text,
    basis                  text NOT NULL,
    valid_from             date,
    valid_to               date,
    needs_review           boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS company_alias (
    rate_id  text NOT NULL REFERENCES measure_rate (rate_id),
    name     text NOT NULL,
    city     text,
    role     text NOT NULL DEFAULT 'producer',
    PRIMARY KEY (rate_id, name)
);
