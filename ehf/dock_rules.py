"""LOCKED facility rules from docks.md (EHF issue #5 P2).

Numbers come from ehf/data/assets.json and the scripted opener unless marked UNKNOWN.
"""

from __future__ import annotations

import json
from datetime import date
from typing import TYPE_CHECKING, Tuple

from ehf.assets import AssetType
from ehf.paths import data_path
from ehf.ships import ShipType

if TYPE_CHECKING:
    from ehf.docks import Docks

# docks.md: Basic Naval Training + Naval Engineering at dock facilities (scripted opener counts).
DOCKS_COMPLETION_CLASS_SLOTS: Tuple[Tuple[str, int], ...] = (
    ("Basic_Naval_Training", 1),
    ("naval_engineering", 9),
)


def docks_build_time_label() -> str:
    with open(data_path("assets.json"), "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return str(data[AssetType.DOCKS.value]["build_time"])


def docks_completion_date(construction_start: date) -> date:
    """Calendar day when a dock asset finishes initial construction (assets.json build_time)."""
    from ehf.assets import Asset

    placeholder = Asset.__new__(Asset)
    return placeholder.calculate_completion_date(construction_start, docks_build_time_label())


def has_large_dock_upgrade(docks: Docks) -> bool:
    return any(
        upgrade.asset_type == AssetType.LARGE_DOCK_UPGRADE and upgrade.Completed()
        for upgrade in docks.upgrades
    )


def operational_drydock_count(docks: Docks) -> int:
    """docks.md: drydock capacity grows via completed dock upgrades (assets.json drydocks fields)."""
    total = 0
    for upgrade in docks.Completed_Upgrades():
        if "drydocks" in upgrade.asset_data:
            total += int(upgrade.asset_data["drydocks"])
    return total


def apply_docks_completion_unlocks(docks: Docks) -> None:
    """Unlock dock-provider naval classes when the dock asset completes (time-based completion)."""
    if not docks.Completed():
        raise ValueError("Dock facility is still under construction.")
    for class_name, count in DOCKS_COMPLETION_CLASS_SLOTS:
        docks.add_class(class_name, count)


def validate_ship_build(docks: Docks, dock_index: int, ship_type: ShipType) -> None:
    """Enforce docks.md ship construction constraints before starting a build."""
    if not docks.Completed():
        raise ValueError("Dock facility must be complete before ship construction.")

    if dock_index < 1 or dock_index > len(docks.drydocks):
        raise ValueError(f"Dock {dock_index} does not exist.")

    if docks.drydocks[dock_index - 1].contains is not None:
        raise ValueError(f"Dock {dock_index} is not empty.")

    if operational_drydock_count(docks) < 1:
        raise ValueError("At least one drydock upgrade is required before ship construction.")

    if ship_type == ShipType.HOSPITAL_SHIP and not has_large_dock_upgrade(docks):
        raise ValueError(
            "HOSPITAL_SHIP requires a completed large_dock_upgrade (docks.md ship types / FR P2)."
        )


def build_ship(docks: Docks, dock_index: int, ship_type: ShipType) -> None:
    validate_ship_build(docks, dock_index, ship_type)
    docks.Build(dock_index, ship_type)
