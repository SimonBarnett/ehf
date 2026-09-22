"""Campaign budget, builds, scorecard, and scripted opener."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Optional

from ehf.assets import AssetType
from ehf.barracks import barracks
from ehf.dock_rules import apply_docks_completion_unlocks
from ehf.docks import Docks
from ehf.engschool import engineering_school
from ehf.paths import data_path
from ehf.ships import ShipType
from ehf.teaching_hospital import teaching_hospital
from ehf.town import Town
from ehf.world import World

DEFAULT_START = date(2019, 7, 31)
DEFAULT_TREASURY = 2_000_000_000

# README operating areas (EHF-L6 CLI deploy target; scoring stub — not a globe UI).
HARDER_DEPLOY_THEATRES = (
    "Cox's Bazar",
    "Juba",
    "Port-au-Prince",
    "Aleppo",
    "Mindanao",
)
DEFAULT_DEPLOY_TARGET = HARDER_DEPLOY_THEATRES[0]

BUILD_MENU = {
    "barracks": (AssetType.BARRACKS, barracks),
    "docks": (AssetType.DOCKS, Docks),
    "engineering_school": (AssetType.ENGINEERING_SCHOOL, engineering_school),
    "teaching_hospital": (AssetType.TEACHING_HOSPITAL, teaching_hospital),
}


def asset_purchase_price(asset_type: AssetType) -> int:
    with open(data_path("assets.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    return int(data[asset_type.value]["initial_purchase_price"])


@dataclass
class Campaign:
    world: World
    treasury: int = DEFAULT_TREASURY
    total_spend: int = 0
    brownfield_used: set[tuple[str, str]] = field(default_factory=set)
    deploy_target: str = DEFAULT_DEPLOY_TARGET

    def can_afford(self, asset_type: AssetType) -> bool:
        return self.treasury >= asset_purchase_price(asset_type)

    def pick_site(self, town: Town, site_index: int = 0) -> dict:
        sites = self.world.towns[town]["brownfield_sites"]
        if site_index < 0 or site_index >= len(sites):
            raise IndexError(f"Brownfield site index {site_index} out of range for {town.value}")
        site = sites[site_index]
        self.brownfield_used.add((town.value, site["name"]))
        return site

    def start_build(
        self,
        town: Town,
        asset_key: str,
        site_index: int = 0,
        on_complete: Optional[Callable] = None,
    ):
        if asset_key not in BUILD_MENU:
            raise ValueError(f"Unknown asset {asset_key}; choose from {list(BUILD_MENU)}")
        asset_type, factory = BUILD_MENU[asset_key]
        price = asset_purchase_price(asset_type)
        if self.treasury < price:
            raise ValueError(f"Insufficient treasury: need £{price:,}, have £{self.treasury:,}")
        site = self.pick_site(town, site_index)
        self.treasury -= price
        self.total_spend += price
        asset = factory(
            self.world,
            site["latitude"],
            site["longitude"],
            OnComplete=on_complete,
        )
        self.world.towns[town]["assets"].append(asset)
        return asset

    def advance_academic_year(self, verbose: bool = False):
        self.world.academic_year(verbose=verbose)

    def count_ships(self) -> int:
        total = 0
        for town in self.world.towns:
            for asset in self.world.towns[town]["assets"]:
                if hasattr(asset, "drydocks"):
                    for dock in asset.drydocks:
                        if dock.contains is not None:
                            total += 1
        return total

    def placement_totals(self) -> tuple[int, int]:
        placed = 0
        capacity = 0
        for town in self.world.towns:
            for asset in self.world.towns[town]["assets"]:
                for slot in getattr(asset, "placements", {}).values():
                    placed += int(slot.get("placed", 0))
                    capacity += int(slot.get("count", 0))
        return placed, capacity

    def completed_training_assets(self) -> int:
        n = 0
        for town in self.world.towns:
            for asset in self.world.towns[town]["assets"]:
                if asset.Completed() and asset.asset_type in {
                    AssetType.BARRACKS,
                    AssetType.DOCKS,
                    AssetType.ENGINEERING_SCHOOL,
                    AssetType.TEACHING_HOSPITAL,
                }:
                    n += 1
        return n

    def scorecard_line(self) -> str:
        placed, capacity = self.placement_totals()
        return (
            f"SCORECARD spend=£{self.total_spend:,} treasury=£{self.treasury:,} "
            f"ships={self.count_ships()} placements={placed}/{capacity} "
            f"brownfield_sites={len(self.brownfield_used)} "
            f"enrolled={len(self.world.e.enrolled)} "
            f"training_assets_complete={self.completed_training_assets()}"
        )

    def docked_ship_lines(self) -> list[str]:
        lines: list[str] = []
        for town in self.world.towns:
            for asset in self.world.towns[town]["assets"]:
                if not hasattr(asset, "drydocks"):
                    continue
                for index, dock in enumerate(asset.drydocks, start=1):
                    if dock.contains is None:
                        continue
                    ship = dock.contains
                    lines.append(
                        f"  {town.value} / {asset.name} drydock {index}: "
                        f"{ship.name} ({ship.type.value})"
                    )
        return lines

    def format_status(self) -> str:
        parts: list[str] = [
            f"Date: {self.world.current_day}  Treasury: £{self.treasury:,}",
            f"Deploy target (stub score): {self.deploy_target}",
        ]
        for town in self.world.towns:
            assets = self.world.towns[town]["assets"]
            if not assets:
                continue
            parts.append(f"\n{town.value}:")
            for asset in assets:
                state = "complete" if asset.Completed() else f"until {asset.completion_date}"
                parts.append(
                    f"  - {asset.name} ({asset.asset_type.value}): {state} "
                    f"lat={asset.latitude} lon={asset.longitude}"
                )
        dock_lines = self.docked_ship_lines()
        if dock_lines:
            parts.append("\nShips in dock:")
            parts.extend(dock_lines)
        if self.world.e.start:
            parts.append(str(self.world.e))
        parts.append(self.scorecard_line())
        return "\n".join(parts)

    def print_status(self):
        print(self.format_status())


def run_blackpool_opener(campaign: Campaign):
    """Scripted Blackpool build sequence (finite, from legacy main.py)."""
    world = campaign.world
    random_site = random.choice(world.towns[Town.BLACKPOOL]["brownfield_sites"])
    campaign.brownfield_used.add((Town.BLACKPOOL.value, random_site["name"]))
    price = asset_purchase_price(AssetType.ENGINEERING_SCHOOL)
    campaign.treasury -= price
    campaign.total_spend += price
    world.towns[Town.BLACKPOOL]["assets"].append(
        engineering_school(
            world,
            random_site["latitude"],
            random_site["longitude"],
            OnComplete=lambda e: (
                e.add_class("civil_engineering", 40)
                or e.upgrade(
                    AssetType.TECHNOLOGY_INSTITUTE,
                    OnComplete=lambda e: (
                        e.add_class("Advanced_Civil_Engineering", 40)
                        or e.upgrade(
                            AssetType.CATERING_UPGRADE,
                            OnComplete=lambda e: (
                                e.add_class("catering", 1)
                                or e.add_class("Advanced_Catering", 1)
                            ),
                        )
                        or e.upgrade(
                            AssetType.LARGE_CLASSROOM_UPGRADE,
                            OnComplete=lambda e: (
                                e.add_class("Advanced_Civil_Engineering", 20)
                                or e.upgrade(
                                    AssetType.LARGE_CLASSROOM_UPGRADE,
                                    OnComplete=lambda e: (
                                        e.add_class("Advanced_Civil_Engineering", 20)
                                        or e.upgrade(
                                            AssetType.LARGE_CLASSROOM_UPGRADE,
                                            OnComplete=lambda e: e.add_class(
                                                "Advanced_Civil_Engineering", 20
                                            ),
                                        )
                                    ),
                                )
                            ),
                        )
                    ),
                )
            ),
        )
    )

    campaign.advance_academic_year()
    campaign.advance_academic_year()
    world.start_enrollment()

    random_site = random.choice(world.towns[Town.BLACKPOOL]["brownfield_sites"])
    campaign.brownfield_used.add((Town.BLACKPOOL.value, random_site["name"]))
    price = asset_purchase_price(AssetType.BARRACKS)
    campaign.treasury -= price
    campaign.total_spend += price
    world.towns[Town.BLACKPOOL]["assets"].append(
        barracks(
            world,
            random_site["latitude"],
            random_site["longitude"],
            OnComplete=lambda b: (
                b.upgrade(
                    AssetType.VR_HALL,
                    OnComplete=lambda b: b.add_class("Advanced_Security_Training", 20),
                )
                or b.upgrade(
                    AssetType.CATERING_UPGRADE,
                    OnComplete=lambda e: (
                        e.add_class("Advanced_Catering", 1)
                        or e.add_class("Advanced_Catering", 1)
                    ),
                )
                or b.add_class("medical", 20)
                or b.add_class("security", 12)
                or b.add_class("IT_and_Communications", 3)
            ),
        )
    )

    campaign.advance_academic_year()
    campaign.advance_academic_year()

    price = asset_purchase_price(AssetType.DOCKS)
    campaign.treasury -= price
    campaign.total_spend += price
    world.towns[Town.BLACKPOOL]["assets"].append(
        Docks(
            world,
            world.towns[Town.BLACKPOOL]["latitude"],
            world.towns[Town.BLACKPOOL]["longitude"],
            OnComplete=lambda d: (
                apply_docks_completion_unlocks(d)
                or d.upgrade(
                    AssetType.CATERING_UPGRADE,
                    OnComplete=lambda e: (
                        e.add_class("Advanced_Catering", 1)
                        or e.add_class("Advanced_Catering", 1)
                    ),
                )
                or d.upgrade(
                    AssetType.NAVAL_SCHOOL,
                    OnComplete=lambda d: (
                        d.add_class("naval_engineering", 20)
                        or d.upgrade(
                            AssetType.LARGE_DOCK_UPGRADE,
                            OnComplete=lambda d: d.Build(1, ShipType.HOSPITAL_SHIP),
                        )
                        or d.upgrade(
                            AssetType.LARGE_CLASSROOM_UPGRADE,
                            OnComplete=lambda d: d.add_class("naval_engineering", 20),
                        )
                        or d.upgrade(
                            AssetType.LARGE_CLASSROOM_UPGRADE,
                            OnComplete=lambda d: d.add_class("Basic_Naval_Training", 20),
                        )
                        or d.upgrade(
                            AssetType.LARGE_CLASSROOM_UPGRADE,
                            OnComplete=lambda d: d.add_class("Advanced_naval_engineering", 20),
                        )
                        or d.upgrade(
                            AssetType.LARGE_CLASSROOM_UPGRADE,
                            OnComplete=lambda d: d.add_class("Advanced_naval_engineering", 20),
                        )
                        or d.upgrade(
                            AssetType.LARGE_CLASSROOM_UPGRADE,
                            OnComplete=lambda d: d.add_class("Advanced_naval_engineering", 20),
                        )
                    ),
                )
            ),
        )
    )

    for _ in range(3):
        campaign.advance_academic_year()

    random_site = random.choice(world.towns[Town.BLACKPOOL]["brownfield_sites"])
    campaign.brownfield_used.add((Town.BLACKPOOL.value, random_site["name"]))
    price = asset_purchase_price(AssetType.TEACHING_HOSPITAL)
    campaign.treasury -= price
    campaign.total_spend += price
    world.towns[Town.BLACKPOOL]["assets"].append(
        teaching_hospital(
            world,
            random_site["latitude"],
            random_site["longitude"],
            OnComplete=lambda h: (
                h.add_class("Advanced_Medical_Training", 50)
                or h.upgrade(
                    AssetType.CATERING_UPGRADE,
                    OnComplete=lambda e: (
                        e.add_class("Advanced_Catering", 1)
                        or e.add_class("Advanced_Catering", 1)
                    ),
                )
            ),
        )
    )


def run_scripted_campaign(years_after_opener: int = 4) -> Campaign:
    world = World(DEFAULT_START)
    campaign = Campaign(world=world)
    run_blackpool_opener(campaign)
    # P1-A2: second town receives a training asset in the same campaign.
    campaign.start_build(Town.JAYWICK, "barracks", site_index=0)
    for _ in range(years_after_opener):
        campaign.advance_academic_year()
    return campaign


def run_until(end: date) -> World:
    world = World(DEFAULT_START)
    while world.current_day < end:
        world.academic_year()
    return world
