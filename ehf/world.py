import json
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from ehf.fleet_member import enlistment
from ehf.paths import data_path
from ehf.town import Town


class World:
    """EHF planning simulation state (import-safe; no scenario runs on construct)."""

    def __init__(self, day: date):
        self.current_day = day
        self.e = enlistment(self.current_day)
        self.towns = {}
        with open(data_path("towns.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
            for town in Town:
                town_data = next(
                    (item for item in data["towns"] if item["name"] == town.value),
                    None,
                )
                if town_data:
                    self.towns[town] = town_data
                    self.towns[town]["assets"] = []

    def find_asset(self, town: Town, asset_type):
        for asset in self.towns[town]["assets"]:
            if asset.asset_type == asset_type:
                return asset
        return None

    def start_enrollment(self):
        self.e.start = True
        self.academic_year()

    def set_current_day(self, day: date, verbose: bool = False):
        for _ in range((day - self.current_day).days):
            self.current_day += timedelta(days=1)
            self.e.set_current_day(self.current_day)
            for town in self.towns:
                for asset in self.towns[town]["assets"]:
                    asset.set_current_day(self.current_day)

        if verbose:
            print(f"\n>>>>>>>> {self.current_day}")
            for town in self.towns:
                for asset in self.towns[town]["assets"]:
                    print(asset)

    def date_add(self, years=0, months=0, weeks=0, days=0):
        d = self.current_day
        d = d + relativedelta(years=years)
        d = d + relativedelta(months=months)
        d = d + timedelta(weeks=weeks)
        d = d + timedelta(days=days)
        self.set_current_day(d)

    def academic_year(self, verbose: bool = False):
        d = self.current_day
        if d.month == 9 and d.day == 1:
            d = d + timedelta(days=1)

        while not (d.month == 9 and d.day == 1):
            d = d + timedelta(days=1)

        self.set_current_day(d, verbose=verbose)
