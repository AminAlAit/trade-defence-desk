"""The shared data shapes (contracts) between the lanes. Issue X-04.

Each lane keeps its own shapes in its own file. Lane A is the contract keeper: after the
freeze, a change needs a pull request approved by all three (docs/08_LANES_AND_ROLES.md).
"""

from trade_defence_desk.contracts.lane_b import (
    Act,
    CompanyAlias,
    Measure,
    MeasureEvent,
    MeasureProduct,
    MeasureRate,
    NameMatch,
)

__all__ = [
    "Act",
    "CompanyAlias",
    "Measure",
    "MeasureEvent",
    "MeasureProduct",
    "MeasureRate",
    "NameMatch",
]
