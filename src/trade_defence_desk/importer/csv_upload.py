"""Read the importer's CSV into Supplier and PurchaseLine (C-13, started early).

The column names are the ones in docs/examples/bergmann_purchase_lines.csv.
Rule from C-13: wrong rows are listed with a reason. One bad row never stops the
upload of the good ones, and nothing is guessed to "repair" a row.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field

from pydantic import ValidationError

from ..contracts.importer import PurchaseLine, Supplier, ValueBasis, supplier_id_for

REQUIRED_COLUMNS = (
    "line_id",
    "description",
    "cn_code",
    "taric_code",
    "supplier_name",
    "supplier_country",
    "producer_name",
    "origin",
    "country_of_dispatch",
    "invoice_declaration_present",
    "annual_customs_value_eur",
    "in_transit_value_eur",
    "incoterm",
)
OPTIONAL_COLUMNS = (
    "value_basis",
    "net_weight_kg",
    "quantity",
    "quantity_unit",
    "supplier_city",
)

_YES = {"yes", "y", "true", "1"}
_NO = {"no", "n", "false", "0"}


@dataclass(frozen=True)
class RowProblem:
    row: int  # 2 is the first data row, as a spreadsheet shows it
    line_id: str | None
    column: str | None
    reason: str
    blocking: bool  # True: the row was not imported. False: imported, with a warning


@dataclass
class UploadReport:
    suppliers: list[Supplier] = field(default_factory=list)
    lines: list[PurchaseLine] = field(default_factory=list)
    problems: list[RowProblem] = field(default_factory=list)

    @property
    def rejected_rows(self) -> list[RowProblem]:
        return [p for p in self.problems if p.blocking]

    @property
    def warnings(self) -> list[RowProblem]:
        return [p for p in self.problems if not p.blocking]


def _empty_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _yes_no(value: str | None) -> bool | None:
    v = (value or "").strip().lower()
    if v in _YES:
        return True
    if v in _NO:
        return False
    return None


def parse_importer_csv(text: str, importer_id: str) -> UploadReport:
    report = UploadReport()
    reader = csv.DictReader(io.StringIO(text))
    header = reader.fieldnames or []
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        report.problems.append(
            RowProblem(1, None, ", ".join(missing), "missing required columns", blocking=True)
        )
        return report

    suppliers: dict[str, Supplier] = {}
    seen_ids: set[str] = set()

    for row_no, row in enumerate(reader, start=2):
        line_id = _empty_to_none(row.get("line_id"))

        if line_id in seen_ids:
            report.problems.append(
                RowProblem(row_no, line_id, "line_id", "duplicate line_id", True)
            )
            continue

        declaration = _yes_no(row.get("invoice_declaration_present"))
        if declaration is None:
            report.problems.append(
                RowProblem(
                    row_no,
                    line_id,
                    "invoice_declaration_present",
                    "must be yes or no",
                    True,
                )
            )
            continue

        try:
            supplier = Supplier(
                id=supplier_id_for(row["supplier_name"] or "", row["supplier_country"] or "xx"),
                importer_id=importer_id,
                name=row["supplier_name"],
                country=row["supplier_country"],
                city=_empty_to_none(row.get("supplier_city")),
            )
            line = PurchaseLine(
                id=line_id or "",
                importer_id=importer_id,
                supplier_id=supplier.id,
                description=row["description"],
                cn_code=_empty_to_none(row["cn_code"]),
                taric_code=_empty_to_none(row["taric_code"]),
                origin=row["origin"],
                country_of_dispatch=row["country_of_dispatch"],
                producer_name=_empty_to_none(row["producer_name"]),
                invoice_declaration_present=declaration,
                annual_customs_value_eur=row["annual_customs_value_eur"],
                value_basis=_empty_to_none(row.get("value_basis")) or ValueBasis.CUSTOMS_VALUE,
                in_transit_value_eur=_empty_to_none(row["in_transit_value_eur"]) or "0",
                incoterm=_empty_to_none(row["incoterm"]),
                net_weight_kg=_empty_to_none(row.get("net_weight_kg")),
                quantity=_empty_to_none(row.get("quantity")),
                quantity_unit=_empty_to_none(row.get("quantity_unit")),
            )
        except ValidationError as exc:
            for err in exc.errors():
                column = ".".join(str(p) for p in err["loc"]) or None
                report.problems.append(RowProblem(row_no, line_id, column, err["msg"], True))
            continue

        seen_ids.add(line.id)
        suppliers.setdefault(supplier.id, supplier)
        report.lines.append(line)

        # Warnings: the row is imported, but the desk will not be able to decide alone.
        if line.effective_cn_code is None:
            report.problems.append(
                RowProblem(
                    row_no,
                    line.id,
                    "cn_code",
                    "no product code: the desk cannot match "
                    "this line by code; add the code to have it checked",
                    False,
                )
            )
        if line.producer_name is None:
            report.problems.append(
                RowProblem(
                    row_no,
                    line.id,
                    "producer_name",
                    "no producer named: the supplier "
                    "name is matched instead, and the case page says so",
                    False,
                )
            )

    report.suppliers = list(suppliers.values())
    return report
