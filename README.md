# EHF — FCDO planning game

**Economic and Humanitarian Fleet** is a CLI strategy sim: stand up training infrastructure in UK seaside towns, run academic years, enroll students, and build ships for humanitarian deployment. The long-form **EHF University** policy proposal lives in [docs/university-proposal.md](docs/university-proposal.md); this file is the game runbook.

## What you are playing

- **Home bases:** seaside towns from `towns.json` (Blackpool, Jaywick, Clacton, Skegness, …).
- **Build:** spend treasury on brownfield sites — barracks, docks, engineering school, teaching hospital (`assets.json`).
- **Time:** the calendar advances one **academic year** (to the next 1 September); assets complete on their `completion_date`.
- **People:** enrollment and specializations use the student pipeline in `classes.json` / `FleetMember`.
- **Output:** docks can produce ships (e.g. hospital ship in `ships.json`).
- **Direction (product intent):** UK training first, then harder humanitarian theatres (Cox's Bazar, Juba, Port-au-Prince, Aleppo, …). Interactive play shows a deploy-target stub on the scorecard; a real globe map is future work.

Data files stay the source of truth; the sim loads them via the `ehf` package (not from arbitrary working directories).

## Setup

```bash
pip install -r requirements.txt
```

Requires Python 3.10+ and `python-dateutil`.

## How to run

From the repository root:

| Command | Purpose |
| --- | --- |
| `python -m ehf --scripted` | Finite acceptance scenario: Blackpool opener plus a barracks build in Jaywick, then four academic years. Prints status and exits. |
| `python -m ehf play` | Interactive campaign (default start **2019-07-31**, treasury **£2,000,000,000**). |
| `python -m ehf --until YYYY-MM-DD` | Advance an empty world to the given date, print date and asset counts, exit. |
| `python -m ehf` | Print CLI help. |

Legacy `python main.py` still exists; prefer `python -m ehf`.

## Interactive rules (`play`)

1. **Treasury:** each new asset deducts its `initial_purchase_price` from `assets.json`. You cannot start a build you cannot afford.
2. **Sites:** `build <town> <asset> [site]` uses brownfield site index `0` by default. Each site can only be used once per campaign.
3. **Towns:** use enum names (e.g. `BLACKPOOL`, `JAYWICK`) or see `towns`.
4. **Assets:** `barracks`, `docks`, `engineering_school`, `teaching_hospital`.
5. **Year:** `year` calls `advance_academic_year()` — construction progresses, completed assets run their upgrade/class hooks.
6. **Enrollment:** `enroll` starts the enrollment phase when you are ready (scripted opener does this automatically).
7. **Status:** `status` prints date, treasury, per-town assets (with lat/lon), ships in dock, enrollment summary, and a **scorecard** (spend, ships, placements, enrolled count, completed training assets).
8. **Exit:** `quit`, `exit`, `q`, or EOF — prints the scorecard and returns.

Example session:

```text
python -m ehf play
> towns
> build JAYWICK barracks 0
> year
> enroll
> status
> quit
```

## Tests

```bash
pytest
```

## Further reading

- Feature roadmap: [docs/feature-request-fcdo-planning-game-2026-09-22.md](docs/feature-request-fcdo-planning-game-2026-09-22.md)
- University proposal (moved from this README): [docs/university-proposal.md](docs/university-proposal.md)
- Facility notes: `docks.md`, `teaching_hospital.md`, `EducationFacilities.md`
