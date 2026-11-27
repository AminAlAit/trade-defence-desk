from trade_defence_desk.importer.csv_upload import parse_importer_csv


def test_bergmann_example_imports_completely(fixtures):
    text = (fixtures / "bergmann_purchase_lines.csv").read_text(encoding="utf-8")
    report = parse_importer_csv(text, "bergmann")
    assert report.rejected_rows == []
    assert [line.id for line in report.lines] == [f"L0{i}" for i in range(1, 10)]
    # L01 and L02 share the fleece code, but L02 comes through a trader.
    l02 = report.lines[1]
    assert l02.producer_name == "Hebei Saikefu Nonwoven Co Ltd"
    assert l02.supplier_id == "cn-ningbo-seaway-trading-co-ltd"
    # Shandong Luye supplies three lines: one supplier row only.
    assert len(report.suppliers) == 7


def test_lines_without_codes_get_a_warning_not_a_rejection(fixtures):
    text = (fixtures / "bergmann_purchase_lines.csv").read_text(encoding="utf-8")
    report = parse_importer_csv(text, "bergmann")
    warned = {p.line_id for p in report.warnings if p.column == "cn_code"}
    assert warned == {"L05", "L06", "L07", "L08"}


def test_bad_rows_are_listed_with_a_reason_and_good_rows_still_import(fixtures):
    text = (fixtures / "bergmann_purchase_lines.csv").read_text(encoding="utf-8")
    lines = text.splitlines()
    bad_decl = lines[1].replace(",yes,", ",maybe,")
    bad_country = lines[2].replace(",CN,CN,no,", ",China,CN,no,", 1)
    duplicate = lines[3]
    text = "\n".join([lines[0], bad_decl, bad_country, lines[3], duplicate])
    report = parse_importer_csv(text, "bergmann")
    reasons = {(p.row, p.column) for p in report.rejected_rows}
    assert (2, "invoice_declaration_present") in reasons
    assert any(row == 3 and col == "origin" for row, col in reasons)
    assert (5, "line_id") in reasons
    assert [line.id for line in report.lines] == ["L03"]


def test_missing_columns_stop_the_upload():
    report = parse_importer_csv("line_id,description\nL01,x\n", "bergmann")
    assert report.lines == []
    assert report.rejected_rows[0].reason == "missing required columns"
