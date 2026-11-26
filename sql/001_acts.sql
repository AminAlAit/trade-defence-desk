-- Group 1 of docs/05_DATA_SCHEMA.md: the acts. Shapes in contracts/lane_b.py (Act)
-- and contracts/lane_a.py (ActSection).

CREATE TABLE IF NOT EXISTS act (
    celex              text PRIMARY KEY,
    kind               text NOT NULL,
    title              text NOT NULL,
    act_type           text NOT NULL,
    type_confidence    text NOT NULL,
    oj_ref             text,
    date_document      date NOT NULL,
    date_publication   date,
    applicable_from    date,
    language           text NOT NULL DEFAULT 'eng',
    source_url         text NOT NULL,
    sha256             text NOT NULL,
    bytes              integer NOT NULL,
    fetched_at         timestamptz NOT NULL,
    is_holdout_hidden  boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS act_section (
    celex       text NOT NULL REFERENCES act (celex),
    section_id  text NOT NULL,
    kind        text NOT NULL,
    "order"     integer NOT NULL,
    text        text NOT NULL,
    PRIMARY KEY (celex, section_id)
);
