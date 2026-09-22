"""CLI: python -m ehf [--until YYYY-MM-DD] | play | scripted | globe"""

import argparse
from datetime import date
from pathlib import Path

from ehf.game import (
    BUILD_MENU,
    Campaign,
    DEFAULT_START,
    DEFAULT_TREASURY,
    run_scripted_campaign,
    run_until,
)
from ehf.globe_map import render_globe_html
from ehf.theatres import god_mode_deploy, list_theatre_choices
from ehf.town import Town
from ehf.world import World


def _parse_date(value: str) -> date:
    y, m, d = (int(part) for part in value.split("-"))
    return date(y, m, d)


def cmd_until(end: date) -> int:
    world = run_until(end)
    print(f"Date: {world.current_day}")
    for town in Town:
        assets = world.towns.get(town, {}).get("assets", [])
        if assets:
            print(f"{town.value}: {len(assets)} assets")
    return 0


def cmd_scripted() -> int:
    campaign = run_scripted_campaign()
    campaign.print_status()
    return 0


def cmd_globe(output: Path, use_scripted: bool) -> int:
    if use_scripted:
        campaign = run_scripted_campaign()
    else:
        campaign = Campaign(world=World(DEFAULT_START), treasury=DEFAULT_TREASURY)
    output.write_text(render_globe_html(campaign), encoding="utf-8")
    print(f"Wrote Earth map to {output.resolve()}")
    return 0


def cmd_play() -> int:
    world = World(DEFAULT_START)
    campaign = Campaign(world=world, treasury=DEFAULT_TREASURY)
    towns = [t for t in Town if t in world.towns]
    print("EHF planning game — type 'help' for commands.")
    while True:
        try:
            line = input("\n> ").strip()
        except EOFError:
            print(campaign.scorecard_line())
            return 0
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        if cmd in ("quit", "exit", "q"):
            print(campaign.scorecard_line())
            return 0
        if cmd == "help":
            print(
                "status | towns | theatres | deploy <id> <graduates|ships|field_team> [n] | "
                "build <town> <asset> [site] | year | enroll | scripted-exit"
            )
            print(f"assets: {', '.join(BUILD_MENU)}")
            continue
        if cmd == "status":
            campaign.print_status()
            continue
        if cmd == "towns":
            for t in towns:
                print(f"  {t.name} ({t.value})")
            continue
        if cmd == "theatres":
            for line in list_theatre_choices(campaign):
                print(line)
            continue
        if cmd == "deploy" and len(parts) >= 3:
            theatre_id = parts[1]
            kind = parts[2].lower()
            count = int(parts[3]) if len(parts) > 3 else 1
            try:
                deployment = god_mode_deploy(campaign, theatre_id, kind, count)
                print(
                    f"Deployed {deployment.kind} ×{deployment.count} to {deployment.theatre_name}."
                )
            except ValueError as exc:
                print(exc)
            continue
        if cmd == "build" and len(parts) >= 3:
            town_key = parts[1].upper().replace("-", "_")
            asset_key = parts[2].lower()
            site = int(parts[3]) if len(parts) > 3 else 0
            try:
                town = Town[town_key]
            except KeyError:
                print(f"Unknown town {parts[1]}")
                continue
            try:
                campaign.start_build(town, asset_key, site_index=site)
                print(f"Started {asset_key} in {town.value} (site {site}).")
            except (ValueError, IndexError) as exc:
                print(exc)
            continue
        if cmd == "year":
            campaign.advance_academic_year()
            print(f"Advanced to {campaign.world.current_day}")
            continue
        if cmd == "enroll":
            campaign.world.start_enrollment()
            print("Enrollment started.")
            continue
        print("Unknown command. Type 'help'.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="EHF FCDO planning game")
    parser.add_argument(
        "--until",
        metavar="YYYY-MM-DD",
        help="Advance empty world to date and exit",
    )
    parser.add_argument(
        "--scripted",
        action="store_true",
        help="Run finite Blackpool opener + Jaywick build (acceptance scenario)",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("play", "globe"),
        help="Interactive turn loop or write Earth map HTML",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("ehf-globe.html"),
        help="Output path for globe HTML (with globe mode)",
    )
    parser.add_argument(
        "--scripted-state",
        action="store_true",
        help="Use scripted campaign state when generating globe HTML",
    )
    args = parser.parse_args(argv)

    if args.until:
        return cmd_until(_parse_date(args.until))
    if args.scripted:
        return cmd_scripted()
    if args.mode == "globe":
        return cmd_globe(args.output, args.scripted_state)
    if args.mode == "play":
        return cmd_play()
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
