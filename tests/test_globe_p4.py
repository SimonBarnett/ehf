from datetime import date
from pathlib import Path

from ehf.game import Campaign, run_scripted_campaign
from ehf.globe_map import render_globe_html
from ehf.theatres import god_mode_deploy, is_theatre_unlocked, load_all_theatres
from ehf.town import Town
from ehf.world import World


def test_theatres_json_loads_uk_and_readme_escalation():
    world = World(date(2019, 7, 31))
    theatres = load_all_theatres(world.towns)
    uk = [t for t in theatres if t.region == "uk"]
    humanitarian = [t for t in theatres if t.region == "humanitarian"]
    assert len(uk) == len([t for t in Town if t in world.towns])
    assert [t.name for t in humanitarian] == [
        "Cox's Bazar",
        "Juba",
        "Port-au-Prince",
        "Aleppo",
        "Mindanao",
    ]
    tiers = [t.difficulty_tier for t in humanitarian]
    assert tiers == [2, 3, 4, 5, 6]


def test_escalating_deploy_unlock():
    world = World(date(2019, 7, 31))
    campaign = Campaign(world=world)
    cox = next(t for t in campaign.globe_theatres if t.id == "coxs_bazar")
    juba = next(t for t in campaign.globe_theatres if t.id == "juba")
    assert not is_theatre_unlocked(cox, campaign)
    god_mode_deploy(campaign, "uk_skegness", "graduates", 5)
    assert is_theatre_unlocked(cox, campaign)
    assert not is_theatre_unlocked(juba, campaign)
    god_mode_deploy(campaign, "coxs_bazar", "field_team", 1)
    assert is_theatre_unlocked(juba, campaign)


def test_globe_html_real_earth_map_surface():
    campaign = run_scripted_campaign(years_after_opener=2)
    html = render_globe_html(campaign)
    assert "leaflet" in html.lower()
    assert "openstreetmap" in html.lower()
    assert "Cox's Bazar" in html
    assert "21.4272" in html


def test_scripted_campaign_globe_deploy_in_status():
    campaign = run_scripted_campaign(years_after_opener=2)
    transcript = campaign.format_status()
    assert "Globe (god-mode)" in transcript
    assert "Deploy target" in transcript
    assert "Cox's Bazar" in transcript
    assert "deploy" in transcript.lower()


def test_globe_cli_writes_file(tmp_path: Path):
    out = tmp_path / "map.html"
    from ehf.__main__ import main

    assert main(["globe", "-o", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "EHF globe" in text
    assert out.stat().st_size > 500
