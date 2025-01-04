
from datetime import date, timedelta
from assets import AssetType , drydock
from EducationalFacilities import EducationalFacilities
from ships import Ship, ShipType , ShipStatus  
    
class Docks(EducationalFacilities):    
    def __init__(self, ehf , latitude , longitude , OnComplete=None):
        super().__init__( AssetType.DOCKS, ehf, latitude , longitude , OnComplete=OnComplete )
        self.drydocks = []

    def __str__(self):
        if not self.Completed():
            return (f"\n{super().__str__()}")                

        docks = "\n\t".join([f"Dock {i+1}: {self.drydocks[i].__str__()}" for i in range(len(self.drydocks))])
        return (f"{super().__str__()}"
                f"\nDrydocks: {len(self.drydocks)}\n\t{docks}"                
        )

    def Build(self, dock , tship: ShipType):
        
        if dock > len(self.drydocks):
            raise ValueError(f"Dock {dock} does not exist.")
        
        if self.drydocks[dock-1].contains != None:           
            raise ValueError(f"Dock {dock} is not empty.")
        
        self.drydocks[dock-1].contains = Ship(
            tship
            , self.current_day
            , self.latitude
            , self.longitude
        )            
                    
    def Add_Placements(self, placements):
        super().Add_Placements(placements)

        for d in (d for d in self.drydocks if d.contains != None):                
            
            if "Naval_Engineering" not in placements:
                placements["Naval_Engineering"] = {}
                placements["Naval_Engineering"]["count"] = 0
                placements["Naval_Engineering"]["placed"] = 0
        
            if d.contains.status == ShipStatus.UNDER_CONSTRUCTION :                                                
                budget = d.contains.cost_price * 0.25 / d.contains._parse_build_time(d.contains.build_time)        
                placements["Naval_Engineering"]["count"] += budget // 1200                        
                                                            
                for e in (e for e in self.ehf.e.enrolled 
                        if e.available <= self.current_day                                   
                        and e.specialization == "Advanced_naval_engineering"                                
                    ):
                    if budget > 1200:                                             
                        e.add_placement(self, "Naval_Engineering_Placement", self.last_day_of_month(self.current_day ))  
                        budget -= 1200
                        placements["Naval_Engineering"]["placed"] += 1
                    
                    else:
                        break
                
                if budget > 1200:                                             
                    for e in (e for e in self.ehf.e.enrolled 
                        if e.available <= self.current_day 
                        and e.meets_requirements(["naval_engineering"])
                        and e.specialization == None
                    ):   
                        if budget > 1200:                                             
                            e.add_placement(self, "Naval_Engineering_Placement", self.last_day_of_month(self.current_day ))  
                            budget -= 1200
                            placements["Naval_Engineering"]["placed"] += 1
                        
                        else:
                            break                    
                
                if budget > 1200:           
                    for e in (e for e in self.ehf.e.enrolled 
                            if e.available <= self.current_day                                   
                            and e.specialization == "Advanced_Civil_Engineering"                                
                        ):
                        if budget > 1200:                                             
                            e.add_placement(self, "Naval_Engineering_Placement", self.last_day_of_month(self.current_day ))  
                            budget -= 1200
                            placements["Naval_Engineering"]["placed"] += 1
                        
                        else:
                            break