# Build and test plan — playable FCDO planning game

**FR:** docs/feature-request-fcdo-planning-game-2026-09-22.md
**Issue:** https://github.com/SimonBarnett/ehf/issues/1
**Park only until dispatched.** This plan is for the first bob-job of #1.

## Scope this job

Ship **P0 + P1** on issue #1. P2/P3 can be nits or Missing features.

11904 campus-pipeline-report (local `6341976`: seeded finite run, scorecard vs README staffing, spend/ships/placements/brownfield) is **P1 acceptance**, not a second FR.

## P0

- `import` of the sim package does not start a scenario or `while True`.
- CLI or `python -m` runs a finite scenario and exits.
- `requirements.txt` includes `python-dateutil`.
- pytest: add one asset, step days, assert completion; process exits.
- Remove `Untitled-*` from git (or gitignore if they must stay local).

## P1

- Turn loop: start date, pick town + site, spend visible budget, advance one academic year, print money / assets / students / ships.
- P1-A1: seeded finite Blackpool (or equivalent) ends with ≥1 completed training asset, non-zero enlistment, process exits.
- P1-A2: a second town can receive an asset in the same campaign.
- Scorecard line (11904): spend, ships, placements, brownfield used; optional note vs README staffing (UNKNOWN if numbers are lore).

## Evidence

- `pytest` (or equivalent) green.
- One CLI/module run transcript showing finite exit + scorecard.
- No secrets. No live FCDO URLs.

## Out of scope this PR

- Full Y1–Y4 / postgraduate pipeline (UNKNOWN).
- Humanitarian theatre score (later).
- Rewriting the university essay in place (P3 = move, not this job unless cheap).
