# Feature request: Make EHF a playable FCDO planning game

**Repo:** https://github.com/SimonBarnett/ehf
**Parked:** 2026-09-22 (marchhare-23624 redo after Simon rejected thin FRs)
**Park only.** Do not dispatch unless asked.
**Credit:** DEV1 16948 critique on IRC (intent / good-bad-ugly / better FRs). 11904 local `1917a99` import-safe runbook is the right *P0 plumbing*, not the product.

## Intent of the project

Repo description is **FCDO Game**. The tree is a prototype of an **Economic and Humanitarian Fleet** planning sim:

- Home bases are left-behind **UK seaside towns** (`towns.json`, `Town` enum: Blackpool, Jaywick, Clacton, Skegness, …).
- The player (implied) **builds training assets** — engineering school, barracks, docks, teaching hospital — on brownfield sites, waits out build time, upgrades (classrooms, catering, VR hall, naval school, large dock).
- **People** (`fleet_member.FleetMember` / `enlistment`) matriculate, take courses, take placements, pick a specialization (year 1–4).
- **Ships** (`ships.json` / `ShipType.HOSPITAL_SHIP`) are the output of docks.
- `README.md` is a long **EHF University** proposal: 4-year paid training (foundation → specialization → fleet tour → civilian transition), postgraduate command/planning/HQ roles, UK public-sector pipeline, and a list of high-impact operating areas (Cox's Bazar, Juba, Haiti, …). FCDO-flavoured: humanitarian + economic development, not a combat navy.

So the *intent* is: **a strategy/planning game that asks “what if we stood up a humanitarian-naval training pipeline from UK coastal towns and deployed the graduates and ships?”** — not a website, not a generic “add tests” chore, and not two unrelated products (policy essay vs broken script) living in one folder forever.

## What's good

- Domain is specific and politically interesting (FCDO + seaside towns + humanitarian fleet).
- Data-driven vocabulary already exists: `towns.json`, `assets.json`, `ships.json`, `classes.json`.
- Time model is real: `current_day`, `AcademicYear` (advance to next 1 Sep), `date_add`, per-asset `build_time` / `completion_date`.
- Asset / upgrade / class names match the README specializations (naval engineering, medical, security, catering, IT, civil engineering).
- Facility sketches in `docks.md`, `teaching_hospital.md`, `EducationFacilities.md` are usable as acceptance seeds.
- `FleetMember` already has year, specialization, prerequisites, placements — a student pipeline, not just buildings.

## What's bad

- **Not a game.** `main.py` is a one-shot Blackpool script: hard-coded asset + nested `or` / lambda upgrade trees, then `while True: AcademicYear()`. No choices, no budget, no win/lose.
- **Cannot import.** Module-level `ehf = main(...)` plus the infinite loop means `import main` never returns. 11904's “import-safe + tests” is necessary plumbing.
- **Broken seams.** `asset()` does `for a in town.assets` on a `Town` enum; `Start_Enrollment` calls global `ehf.AcademicYear()`; `class main` shadows the idea of a program entry.
- **README is not engineering.** It is a university/policy essay. No how-to-run, no rules of the game, no “what this repo is”.
- **No package, no deps, no tests, no CI.** `python-dateutil` is imported; nothing declares it. No `requirements.txt`, no pytest, no golden day.
- **Scratch in git.** `Untitled-1.dart`, `Untitled-2.json` … `Untitled-5.py`.

## What's ugly

- **Two products, neither finished.** The university proposal (staffing tables, Starlink, 3D-object DB, postgraduate command roles, Cox's Bazar) never meets the Python sim. The sim never scores a humanitarian deployment.
- **Only Blackpool is played.** Twenty towns in the enum; one town gets buildings.
- **CWD-relative JSON** (`open("towns.json")`) so the sim only works from repo root.
- **Construction API is unreadable.** Nested `OnComplete=lambda` / `or` chains are untestable and hide the intended build order.

## What would make it better (concrete features)

These are the product FRs, in order. Do not park a second “add tests” issue as the whole job.

### P0 — Import-safe package + one golden year (plumbing)

- Package the sim so `import ehf` does not start a scenario or loop.
- CLI: `python -m ehf --until 2020-09-01` (or equivalent) prints the day and assets and exits.
- `requirements.txt` (at least `python-dateutil`).
- pytest: construct world, add one asset, step N days, assert completion_date / not-infinite.
- Delete or `.gitignore` `Untitled-*`.
- This is 11904 `1917a99` / “sim-runbook+tests+import-safe”. Keep it as the first slice of *this* FR, not a separate product.

### P1 — Playable FCDO turn loop (the actual feature)

A human can play a short campaign:

1. Start on a date (default 2019-07-31 as today).
2. Pick a seaside town and a brownfield site.
3. Spend a visible budget to start one asset (barracks / docks / eng-school / teaching hospital).
4. Advance one academic year.
5. See: money left, assets complete/in-progress, enrolled students by specialization, ships in dock.

Acceptance (P1-A1): after a scripted 4-year Blackpool opener *or* a player-driven equivalent, the printed state includes at least one completed training asset and a non-zero enlistment count, and the process exits.

Acceptance (P1-A2): a second town can receive an asset in the same campaign (not Blackpool-only).

### P2 — Wire one facility doc as rules

Pick `docks.md` (or teaching hospital) and encode 2–3 LOCKED rules as tests (e.g. docks unlock a class after N days; large-dock upgrade is required before `HOSPITAL_SHIP`). Proposal numbers that are not in code stay UNKNOWN.

### P3 — Split the two documents

- `README.md` = what the game is, how to run, rules.
- `docs/university-proposal.md` = the existing EHF University essay (moved, not rewritten as fiction).

### Later (UNKNOWN until P1 exists)

- Humanitarian deployment score (ship leaves, impact on a named theatre).
- Full Y1–Y4 / postgraduate pipeline from the proposal.
- Multiplayer / FCDO workshop mode.

## Gap vs current tree

| In tree | Missing vs intent |
| --- | --- |
| `main.py` Blackpool script + `while True` | Player turns, budget, exit |
| `Town` + `towns.json` | Any town except Blackpool actually built |
| `Asset` / upgrades / classes | Readable build orders; tests |
| `FleetMember` year + specialization | Game-visible enrollment / career output |
| `ShipType` + dock `Build` | Mission / deployment |
| README university essay | Game rules + runbook |
| `Untitled-*` | Gone |
| (no tests, no deps file) | P0 |

## LOCKED

- EHF-L1: Product intent is an FCDO-flavoured **planning game** (towns → training assets → people → ships), not a CMS and not “tests only”.
- EHF-L2: Do not break or discard `towns.json` / `assets.json` / `ships.json` / `classes.json` as the data model.
- EHF-L3: Do not invent instance URLs, secrets, or live FCDO systems.
- EHF-L4: P0 import-safe + one test is required plumbing; it is not the whole FR.
- EHF-L5: Park only until Simon says bob-job / dispatch.

## UNKNOWN

- U1: Turn UI (CLI vs later GUI). P1 can be CLI.
- U2: Budget units and starting treasury.
- U3: Whether university staffing tables are simulated or stay lore.
- U4: Whether 11904's local `1917a99` branch can be pushed from DEV1 or must be re-done here.

## Phase order

1. P0 import-safe + golden year + delete Untitled + requirements.
2. P1 playable turn loop (multi-town, budget, students, ships, exits).
3. P2 one facility md as acceptance.
4. P3 split README vs university proposal.
5. Later: deployment score / full pipeline (unknowns).
