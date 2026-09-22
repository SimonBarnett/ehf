from datetime import date, timedelta

import pytest

from ehf.assets import AssetType
from ehf.dock_rules import (
    DOCKS_COMPLETION_CLASS_SLOTS,
    apply_docks_completion_unlocks,
    build_ship,
    docks_completion_date,
    operational_drydock_count,
    validate_ship_build,
)
from ehf.docks import Docks
from ehf.ships import ShipType
from ehf.town import Town
from ehf.world import World


def _append_docks(world: World, on_complete=None) -> Docks:
    site = world.towns[Town.BLACKPOOL]["brownfield_sites"][0]
    docks = Docks(
        world,
        site["latitude"],
        site["longitude"],
        OnComplete=on_complete,
    )
    world.towns[Town.BLACKPOOL]["assets"].append(docks)
    return docks


def _advance_to(world: World, day: date) -> None:
    world.set_current_day(day)


def test_docks_unlock_naval_classes_after_build_time():
    start = date(2019, 7, 31)
    world = World(start)
    docks = _append_docks(world)
    assert not docks.Completed()
    completion = docks_completion_date(start)
    assert completion == docks.completion_date

    _advance_to(world, completion - timedelta(days=1))
    assert not docks.Completed()

    _advance_to(world, completion)
    apply_docks_completion_unlocks(docks)
    offered = docks.all_classes()
    for class_name, expected in DOCKS_COMPLETION_CLASS_SLOTS:
        assert offered[class_name]["count"] == expected


def test_hospital_ship_requires_large_dock_upgrade():
    world = World(date(2019, 7, 31))
    docks = _append_docks(world)
    _advance_to(world, docks.completion_date)

    docks.upgrade(AssetType.DOCK_UPGRADE)
    small_dock = docks.upgrades[-1]
    _advance_to(world, small_dock.completion_date)
    assert operational_drydock_count(docks) >= 1

    with pytest.raises(ValueError, match="large_dock_upgrade"):
        validate_ship_build(docks, 1, ShipType.HOSPITAL_SHIP)

    docks.upgrade(AssetType.LARGE_DOCK_UPGRADE)
    large_dock = docks.upgrades[-1]
    _advance_to(world, large_dock.completion_date)

    build_ship(docks, 1, ShipType.HOSPITAL_SHIP)
    assert docks.drydocks[0].contains.type == ShipType.HOSPITAL_SHIP


def test_one_ship_per_drydock():
    world = World(date(2019, 7, 31))
    docks = _append_docks(world)
    _advance_to(world, docks.completion_date)
    docks.upgrade(AssetType.LARGE_DOCK_UPGRADE)
    large_dock = docks.upgrades[-1]
    _advance_to(world, large_dock.completion_date)

    build_ship(docks, 1, ShipType.UTILITY_BOAT)
    with pytest.raises(ValueError, match="not empty"):
        validate_ship_build(docks, 1, ShipType.FRIGATE)
