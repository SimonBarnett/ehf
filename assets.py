import json
from enum import Enum
import random
from datetime import date, timedelta

class drydock:
    def __init__(self):
        self.contains = None

    def __str__(self):
        return f"{self.contains.name} ({self.contains.type.value})" if self.contains != None else "Empty"    
    
class AssetType(Enum):
    
    HEADQUARTERS = "headquarters"
    OPERATIONS_ROOM_UPGRADE = "operations_room_upgrade"
    PLANNING_STAFF_UPGRADE = "planning_staff_upgrade"        
    LECTURE_HALL = "lecture_hall"
    
    ENGINEERING_SCHOOL = "Engineering_School"
    TECHNOLOGY_INSTITUTE = "Technology_Institute"
    
    DOCKS = "docks"
    DOCK_UPGRADE = "dock_upgrade"
    LARGE_DOCK_UPGRADE = "large_dock_upgrade"
    NAVAL_SCHOOL = "naval_school"
    
    BARRACKS = "barracks"
    VR_HALL = "vr_hall"

    TEACHING_HOSPITAL = "teaching_hospital"
    
    WAREHOUSE = "warehouse"    
    WAREHOUSE_UPGRADE = "warehouse_upgrade"
    
    # General Upgrades
    CATERING_UPGRADE = "catering_upgrade"
    SMALL_CLASSROOM_UPGRADE = "small_classroom_upgrade"
    LARGE_CLASSROOM_UPGRADE = "large_classroom_upgrade"

class Asset():    
    def __init__(self, asset_type, ehf, OnComplete = None, latitude: float = None, longitude: float = None):
        
        self.ehf = ehf
        self.asset_type = asset_type
        self.current_day = self.ehf.current_day
        self.construction_start_date = self.ehf.current_day
        self.latitude = latitude
        self.longitude = longitude    
        self.employed = []
        self.placements = {}        
        self.upgrades = []
        self.OnComplete = OnComplete
        self.parent = None

        with open("assets.json", 'r') as f:                    
            data = json.load(f)        
            for this_asset, asset_data in data.items():
                if asset_type.value == this_asset:                
                    self.initial_purchase_price = asset_data["initial_purchase_price"]
                    self.daily_maintenance = asset_data["daily_maintenance"]
                    self.annual_maintenance = asset_data["daily_maintenance"] * 365
                    self.build_time = asset_data["build_time"]                    
                    if "upgrades" in asset_data:
                        self.upgrades = asset_data["upgrades"]
                    else:
                        self.completion_date = self.calculate_completion_date(self.construction_start_date, self.build_time)   
                    
                    if "names" in asset_data:
                        self.name = random.choice(asset_data["names"])
                    else:
                        self.name = self.asset_type.value

                    self.asset_data = asset_data                                                 
                    break

    def __str__(self):
        if self.completion_date > self.current_day:    
            return (
                f"{self.name} - Completion Date: {self.completion_date}"
                f"{self.placements_str()}"
            )        
        else:               
            return (
                f"{self.name}"                
            )        

    def students(self):
        return 0
    
    def placements_str(self):
        if not self.isUpgrade():
            pl = self.placements        
            for u in self.upgrades:
                for k, v in u.placements.items():
                    if not k in pl:
                        pl[k] = {}                    
                        pl[k]["count"] = 0
                        pl[k]["placed"] = 0

                    pl[k]["count"] += v["count"]
                    pl[k]["placed"] += v["placed"]

            return f"\nPlacements: {', '.join([f'{k}: ({v["placed"]}/{int(v["count"])})' for k, v in pl.items()])}"
        return ""
    
    def facilities_Maintaiance(self):
        r = 0
        if self.Completed():
            r += self.daily_maintenance
            for each in self.Completed_Upgrades():
                r += each.daily_maintenance
        return r * 365
    
    def isUpgrade(self):
        return "upgrades" in self.asset_data
    
    def upgrades_str(self):
        if not self.isUpgrade():
            if self.upgrades:
                # Convert upgrades to a list of unique upgrades while maintaining order
                unique_upgrades = []
                seen = set()
                upgrade_counts = {}
                for upgrade in self.upgrades:
                    if upgrade.__str__() not in seen:
                        upgrade_counts[upgrade.__str__()] = 1
                        unique_upgrades.append(upgrade.__str__())
                        seen.add(upgrade.__str__())
                    else:
                        upgrade_counts[upgrade.__str__()] += 1

                # Format the string with counts
                formatted_upgrades = []
                for upgrade in unique_upgrades:
                    count = upgrade_counts[upgrade]
                    formatted_upgrades.append(f"{count} * {upgrade.__str__()}")
                
                return f"\nUpgrades: \n\t{'\n\t'.join(formatted_upgrades)}"
        return ""

    def upgrade(self, type: AssetType, OnComplete=None):
        upgrade = Asset(type, self.ehf, self.current_day, self.latitude, self.longitude)

        if not "upgrades" in upgrade.asset_data:
            raise ValueError(f"{upgrade.asset_type.name} is not an upgrade.")
        elif not self.asset_type.value in upgrade.upgrades:
            raise ValueError(f"{upgrade.asset_type.name} cannot upgrade {self.asset_type.name}.")
        elif not self.Completed():
            raise ValueError(f"{self.asset_type.name} is still being built.")
        else:
            upgrade.parent = self
            upgrade.OnComplete = OnComplete
            upgrade.current_day = self.current_day
            upgrade.construction_start_date = upgrade.current_day            
            upgrade.completion_date = self.calculate_completion_date(upgrade.construction_start_date, upgrade.build_time) 
            self.upgrades.append(upgrade)
            
    def Wages(self):
        wage = 0
        for i in self.employed:
            wage += (i["count"] * i["wage"])
        return wage
    
    def set_current_day(self, day: date):    

        comp = self.Completed()
        self.current_day = day        
        if not comp and self.Completed():                        
            # Asset completed
            if self.parent != None:                    
                if "drydocks" in self.parent.asset_data:
                    c = 0
                    for u in self.parent.Completed_Upgrades():
                        if "drydocks" in u.asset_data:
                            c += u.asset_data["drydocks"]
                    
                    for i in range(1, c+1):
                        if len(self.parent.drydocks) < i :
                            self.parent.drydocks.append( drydock() )
                                                
                self.parent.all_classes()
                if self.OnComplete != None: self.OnComplete(self.parent)

            else:
                self.all_classes()
                if self.OnComplete != None: self.OnComplete(self)                

        if not self.isUpgrade():
            for u in self.upgrades:
                u.set_current_day(day)

        # Assign placements
        if self.current_day.day == 2 :
            if not self.isUpgrade():
                for p in self.placements:
                    self.placements[p]["placed"] = 0
                    self.placements[p]["count"] = 0
                
                self.Add_Placements(self.placements)
                for u in self.upgrades:
                    u.Add_Placements(self.placements)
                    
                for u in (u for u in self.Completed_Upgrades() if u.name == "catering_upgrade"):                    
                    self.Add_Catering(self.placements, self.students() + sum(placements["placed"] for placements in self.placements.values()))

    def Add_Catering(self, placements, seats):  

        s = seats // 20

        if "Catering" not in placements :
            placements["Catering"] = {}
            placements["Catering"]["count"] = 0
            placements["Catering"]["placed"] = 0

        placements["Catering"]["count"] += s

        for e in (e for e in self.ehf.e.enrolled 
            if e.available <= self.current_day 
            and e.specialization == "Advanced_Catering"
        ):   
            if s > 0:                                 
                e.add_placement(self, f"Catering_Placement", self.last_day_of_month(self.current_day))  
                s-=1
                placements["Catering"]["placed"] += 1                    

            else:
                break
        
        if s > 0:   
            for e in (e for e in self.ehf.e.enrolled 
                if e.available <= self.current_day 
                and e.meets_requirements(["catering"])
            ):   
                if s > 0:                                 
                    e.add_placement(self, f"Catering_Placement", self.last_day_of_month(self.current_day))  
                    s-=1
                    placements["Catering"]["placed"] += 1                    

                else:
                    break    

    def Add_Placements(self, placements):
    
        if "Civil_Engineering" not in placements :
            placements["Civil_Engineering"] = {}
            placements["Civil_Engineering"]["count"] = 0
            placements["Civil_Engineering"]["placed"] = 0
        
        if not self.Completed():
            budget = self.initial_purchase_price * 0.25 / int(self.build_time.split(" ")[0])
        else:
            budget = .8 * (self.annual_maintenance / 12)
        
        placements["Civil_Engineering"]["count"] += budget // 1200

        for e in (e for e in self.ehf.e.enrolled if e.available <= self.current_day and e.specialization == "Advanced_Civil_Engineering"):   
            if budget > 1200:                                 
                e.add_placement(self, f"Civil_Engineering_Placement", self.last_day_of_month(self.current_day))  
                budget -= 1200                                                                  
                placements["Civil_Engineering"]["placed"] += 1                    

            else:
                break
        
        if budget > 1200:   
            for e in (e for e in self.ehf.e.enrolled if e.available <= self.current_day and e.meets_requirements(["Civil_Engineering"])):   
                if budget > 1200:                                 
                    e.add_placement(self, f"Civil_Engineering_Placement", self.last_day_of_month(self.current_day))  
                    budget -= 1200                                                                  
                    placements["Civil_Engineering"]["placed"] += 1                    

                else:
                    break                
        
        if self.Completed():                                
            if "Force_Protection" not in placements:
                placements["Force_Protection"] = {}
                placements["Force_Protection"]["count"] = 0
                placements["Force_Protection"]["placed"] = 0
            
            # Security budget
            budget = .2 * (self.annual_maintenance / 12)
            placements["Force_Protection"]["count"] += budget // 1200
                        
            for e in (e for e in self.ehf.e.enrolled if e.available <= self.current_day and e.specialization == "Advanced_Security_Training"):   
                if budget > 1200:                                 
                    e.add_placement(self, f"Force_Protection", self.last_day_of_month(self.current_day))  
                    budget -= 1200                                                                  
                    placements["Force_Protection"]["placed"] += 1                    

                else:
                    break              

    #region Calculate Completion Date

    def last_day_of_month(self, any_date):
        next_month = any_date.replace(day=28) + timedelta(days=4)  # this will never fail
        return next_month - timedelta(days=next_month.day)

    def Completed_Upgrades(self):
        return [upgrade for upgrade in self.upgrades if upgrade.completion_date <= self.current_day]

    def Completed(self):
        return self.completion_date <= self.current_day
    
    def calculate_completion_date(self, construction_start_date: date, build_time: str) -> date:
        """
        Calculate the completion date based on the construction start date and build time.

        :param construction_start_date: Date when construction begins
        :param build_time: String describing the duration of construction, e.g., "2 years, 3 months", "12 months"
        :return: The estimated completion date
        """
        months_to_add = 0
        years_to_add = 0

        # Split the build_time into components
        time_components = build_time.split(', ')
        for component in time_components:
            quantity, unit = component.split()
            quantity = int(quantity)
            if unit.startswith('year'):
                years_to_add += quantity
            elif unit.startswith('month'):
                months_to_add += quantity
            else:
                raise ValueError(f"Unrecognized time unit in build time: {component}")

        # First add years, then add months
        completion_date = construction_start_date.replace(year=construction_start_date.year + years_to_add)
        completion_date = self.add_months(completion_date, months_to_add)

        return completion_date

    def add_months(self, source_date, months):
        """
        Add a number of months to the source date, accounting for varying month lengthsand leap years.

        :param source_date: The original date
        :param months: Number of months to add
        :return: New date after adding months
        """
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        if month == 2 and day == 29 and not self.is_leap_year(year):
            day = 28
        return date(year, month, day)

    def is_leap_year(self, year):
        """
        Check if a given year is a leap year.

        :param year: The year to check
        :return: True if it's a leap year, False otherwise
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    #endregion
