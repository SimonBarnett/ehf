import json
from enum import Enum
import random

from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

from fleet_member import enlistment
from assets import Asset , AssetType
from ships import ShipType
from barracks import barracks
from Docks import Docks
from teaching_hospital import teaching_hospital
from engschool import engineering_school

class Town(Enum):
    BLACKPOOL = "Blackpool"
    JAYWICK = "Jaywick"
    CLACTON_ON_SEA = "Clacton-on-Sea"
    SKEGNESS = "Skegness"
    RHYL = "Rhyl"
    MARGATE = "Margate"
    GREAT_YARMOUTH = "Great Yarmouth"
    GRIMSBY = "Grimsby"
    SCARBOROUGH = "Scarborough"
    BRIDLINGTON = "Bridlington"
    HASTINGS = "Hastings"
    MORECAMBE = "Morecambe"
    CLEETHORPES = "Cleethorpes"
    SOUTH_SHIELDS = "South Shields"
    WHITSTABLE = "Whitstable"
    BOGNOR_REGIS = "Bognor Regis"
    REDCAR = "Redcar"
    HARTLEPOOL = "Hartlepool"
    LOWESTOFT = "Lowestoft"
    SOUTHPORT = "Southport"

class main():

    def __init__(self , day: date):
        self.current_day = day        
        self.e = enlistment(self.current_day)
        self.towns = {}
        with open("towns.json", 'r') as f:
            data = json.load(f)
            for town in Town:
                # Find the town in the data list by matching the name
                town_data = next((item for item in data['towns'] if item['name'] == town.value), None)
                if town_data:
                    self.towns[town] = town_data
                    self.towns[town]["assets"] = []                    
    
    def asset(self, town: Town, type: AssetType):        
        for a in town.assets:
            if a.type == type:
                return a
                
    def Start_Enrollment(self):
        self.e.start = True
        ehf.AcademicYear()        

    def set_current_day(self, day: date):
        for i in range((day - self.current_day).days):                              
            self.current_day += timedelta(days=1)
            
            self.e.set_current_day(self.current_day)

            for t in self.towns:
                for a in self.towns[t]["assets"]:
                    a.set_current_day(self.current_day)            
        
        print(f"\n>>>>>>>> {self.current_day}")
        for t in self.towns:
            for a in self.towns[t]["assets"]:
                print(a)
        
        #if self.e.start : print(self.e)            

    def date_add(self , years = 0 , months=0 , weeks=0, days=0):
        d = self.current_day
        d = d + relativedelta(years=years)
        d = d + relativedelta(months=months)
        d = d + timedelta(weeks=weeks)
        d = d + timedelta(days=days)
        
        self.set_current_day( d )

    def AcademicYear(self):
        d = self.current_day
        if (d.month == 9 and d.day == 1):
            d = d + timedelta(days=1)

        while not (d.month == 9 and d.day == 1):
            d = d + timedelta(days=1)

        self.set_current_day( d )        

    

print(">")
ehf = main(date(2019, 7, 31))

random_site = random.choice(ehf.towns[Town.BLACKPOOL]["brownfield_sites"])
ehf.towns[Town.BLACKPOOL]["assets"].append(
    engineering_school(ehf, random_site["latitude"], random_site["longitude"], OnComplete=lambda e: 
        e.add_class("civil_engineering", 40)
        or e.upgrade(AssetType.TECHNOLOGY_INSTITUTE, OnComplete=lambda e: 
            e.add_class("Advanced_Civil_Engineering", 40)          
            or e.upgrade(AssetType.CATERING_UPGRADE, OnComplete=lambda e:        
                e.add_class("catering",1)
                or e.add_class("Advanced_Catering",1) 
            )                         
            or e.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda e: 
                e.add_class("Advanced_Civil_Engineering",20)
                or e.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda e: 
                    e.add_class("Advanced_Civil_Engineering",20
                    or e.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda e: 
                        e.add_class("Advanced_Civil_Engineering",20)
                    )
                ))
            )                     
        )            
    )
)

ehf.AcademicYear()
ehf.AcademicYear()
ehf.Start_Enrollment()

random_site = random.choice(ehf.towns[Town.BLACKPOOL]["brownfield_sites"])
ehf.towns[Town.BLACKPOOL]["assets"].append(
    barracks(ehf,random_site["latitude"], random_site["longitude"], OnComplete=lambda b:
        b.upgrade(AssetType.VR_HALL, OnComplete=lambda b:
            b.add_class("Advanced_Security_Training",20)    
        )     
        or b.upgrade(AssetType.CATERING_UPGRADE, OnComplete=lambda e:        
            e.add_class("Advanced_Catering",1)
            or e.add_class("Advanced_Catering",1) 
        )                                
        or b.add_class("medical",20)
        or b.add_class("security",12)        
        or b.add_class("IT_and_Communications",3)                                              
    )
)

ehf.AcademicYear()
ehf.AcademicYear()

ehf.towns[Town.BLACKPOOL]["assets"].append(
    Docks(ehf, ehf.towns[Town.BLACKPOOL]["latitude"], ehf.towns[Town.BLACKPOOL]["longitude"], OnComplete=lambda d:
        d.add_class("Basic_Naval_Training",1)
        or d.add_class("naval_engineering",9)
        or d.upgrade(AssetType.CATERING_UPGRADE, OnComplete=lambda e:        
            e.add_class("Advanced_Catering",1)
            or e.add_class("Advanced_Catering",1) 
        )            
        or d.upgrade(AssetType.NAVAL_SCHOOL,OnComplete=lambda d:
            d.add_class("naval_engineering",20)
            or d.upgrade(AssetType.LARGE_DOCK_UPGRADE, OnComplete=lambda d: d.Build(1, ShipType.HOSPITAL_SHIP))
            or d.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda d: d.add_class("naval_engineering",20))
            or d.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda d: d.add_class("Basic_Naval_Training",20))
            or d.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda d: d.add_class("Advanced_naval_engineering",20))
            or d.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda d: d.add_class("Advanced_naval_engineering",20))
            or d.upgrade(AssetType.LARGE_CLASSROOM_UPGRADE, OnComplete=lambda d: d.add_class("Advanced_naval_engineering",20))
        )                            
    )
)

ehf.AcademicYear()
ehf.AcademicYear()
ehf.AcademicYear()

random_site = random.choice(ehf.towns[Town.BLACKPOOL]["brownfield_sites"])
ehf.towns[Town.BLACKPOOL]["assets"].append(
    teaching_hospital(ehf, random_site["latitude"], random_site["longitude"], OnComplete=lambda h:
        h.add_class("Advanced_Medical_Training",50)                          
        or h.upgrade(AssetType.CATERING_UPGRADE, OnComplete=lambda e:        
            e.add_class("Advanced_Catering",1)
            or e.add_class("Advanced_Catering",1) 
        )            
    )
)

while True:
    ehf.AcademicYear()
    print(ehf.e)    
