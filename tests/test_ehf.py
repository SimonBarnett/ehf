from datetime import date

import ehf
from ehf.assets import AssetType
from ehf.barracks import barracks
from ehf.game import Campaign, asset_purchase_price, run_scripted_campaign
from ehf.town import Town
from ehf.world import World


def test_import_does_not_run_scenario():
    assert ehf.World is not None
    assert ehf.Town.BLACKPOOL.value == "Blackpool"


def test_add_asset_and_step_to_completion():
    world = World(date(2019, 7, 31))
    site = world.towns[Town.BLACKPOOL]["brownfield_sites"][0]
    asset = barracks(world, site["latitude"], site["longitude"])
    world.towns[Town.BLACKPOOL]["assets"].append(asset)
    assert not asset.Completed()
    world.set_current_day(asset.completion_date)
    assert asset.Completed()


def test_run_until_exits():
    end = date(2020, 9, 1)
    world = ehf.run_until(end)
    assert world.current_day >= end


def test_scripted_campaign_acceptance():
    campaign = run_scripted_campaign(years_after_opener=4)
    assert campaign.completed_training_assets() >= 1
    assert len(campaign.world.e.enrolled) > 0
    jaywick_assets = campaign.world.towns[Town.JAYWICK]["assets"]
    assert len(jaywick_assets) >= 1
    assert jaywick_assets[0].asset_type == AssetType.BARRACKS


def test_campaign_budget_deduction():
    world = World(date(2019, 7, 31))
    campaign = Campaign(world=world, treasury=asset_purchase_price(AssetType.BARRACKS))
    campaign.start_build(Town.SKEGNESS, "barracks", site_index=0)
    assert campaign.treasury == 0
    assert campaign.total_spend == asset_purchase_price(AssetType.BARRACKS)
