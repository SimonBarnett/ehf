"""Globe theatres: UK training hubs + escalating README humanitarian areas."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Literal

from ehf.paths import data_path
from ehf.town import Town

if TYPE_CHECKING:
    from ehf.game import Campaign

DeployKind = Literal["graduates", "ships", "field_team"]

_DEPLOY_KINDS: tuple[DeployKind, ...] = ("graduates", "ships", "field_team")


@dataclass(frozen=True)
class Theatre:
    id: str
    name: str
    latitude: float
    longitude: float
    difficulty_tier: int
    region: str
    notes: str = ""

    @property
    def is_uk_training(self) -> bool:
        return self.region == "uk"


@dataclass
class Deployment:
    theatre_id: str
    theatre_name: str
    kind: DeployKind
    count: int
    day: str
    latitude: float
    longitude: float
    difficulty_tier: int


def _load_humanitarian_rows() -> list[dict]:
    with open(data_path("theatres.json"), "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return list(payload["humanitarian_theatres"])


def load_all_theatres(world_towns: dict) -> list[Theatre]:
    theatres: list[Theatre] = []
    for town in Town:
        if town not in world_towns:
            continue
        row = world_towns[town]
        theatres.append(
            Theatre(
                id=f"uk_{town.name.lower()}",
                name=f"{town.value} (UK training)",
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                difficulty_tier=1,
                region="uk",
                notes="Seaside training base",
            )
        )
    for row in _load_humanitarian_rows():
        theatres.append(
            Theatre(
                id=row["id"],
                name=row["name"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                difficulty_tier=int(row["difficulty_tier"]),
                region="humanitarian",
                notes=str(row.get("notes", "")),
            )
        )
    return theatres


def theatre_by_id(theatres: Iterable[Theatre]) -> dict[str, Theatre]:
    return {t.id: t for t in theatres}


def deployed_tiers(campaign: Campaign) -> set[int]:
    return {d.difficulty_tier for d in campaign.deployments}


def is_theatre_unlocked(theatre: Theatre, campaign: Campaign) -> bool:
    if theatre.difficulty_tier <= 1:
        return True
    required = theatre.difficulty_tier - 1
    return required in deployed_tiers(campaign)


def unlocked_theatres(campaign: Campaign) -> list[Theatre]:
    return [t for t in campaign.globe_theatres if is_theatre_unlocked(t, campaign)]


def next_locked_theatre(campaign: Campaign) -> Theatre | None:
    for theatre in sorted(
        (t for t in campaign.globe_theatres if not is_theatre_unlocked(t, campaign)),
        key=lambda t: t.difficulty_tier,
    ):
        return theatre
    return None


def recommend_deploy_target(campaign: Campaign) -> str:
    """Player-facing next theatre name (escalating difficulty)."""
    locked = next_locked_theatre(campaign)
    if locked is not None:
        return locked.name
    if campaign.deployments:
        return campaign.deployments[-1].theatre_name
    return "Blackpool (UK training)"


def god_mode_deploy(
    campaign: Campaign,
    theatre_id: str,
    kind: DeployKind,
    count: int = 1,
) -> Deployment:
    if kind not in _DEPLOY_KINDS:
        raise ValueError(f"kind must be one of {_DEPLOY_KINDS}")
    if count < 1:
        raise ValueError("count must be at least 1")
    lookup = theatre_by_id(campaign.globe_theatres)
    theatre = lookup.get(theatre_id)
    if theatre is None:
        raise ValueError(f"Unknown theatre id {theatre_id}")
    if not is_theatre_unlocked(theatre, campaign):
        raise ValueError(
            f"Theatre {theatre.name} (tier {theatre.difficulty_tier}) is locked; "
            f"deploy to tier {theatre.difficulty_tier - 1} first."
        )
    if kind == "ships" and campaign.count_ships() < count:
        raise ValueError(
            f"Need {count} ship(s) in dock for deployment; have {campaign.count_ships()}."
        )
    deployment = Deployment(
        theatre_id=theatre.id,
        theatre_name=theatre.name,
        kind=kind,
        count=count,
        day=str(campaign.world.current_day),
        latitude=theatre.latitude,
        longitude=theatre.longitude,
        difficulty_tier=theatre.difficulty_tier,
    )
    campaign.deployments.append(deployment)
    campaign.deploy_target = theatre.name
    return deployment


def list_theatre_choices(campaign: Campaign) -> list[str]:
    lines: list[str] = []
    for theatre in sorted(campaign.globe_theatres, key=lambda t: (t.difficulty_tier, t.name)):
        flag = "unlocked" if is_theatre_unlocked(theatre, campaign) else "locked"
        lines.append(
            f"  {theatre.id}: {theatre.name} tier={theatre.difficulty_tier} [{flag}] "
            f"lat={theatre.latitude} lon={theatre.longitude}"
        )
    return lines
