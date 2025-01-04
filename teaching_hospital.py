from datetime import date, timedelta
from assets import AssetType
from EducationalFacilities import EducationalFacilities

class teaching_hospital(EducationalFacilities):
    def __init__(self, ehf , latitude , longitude, OnComplete=None):
        super().__init__( AssetType.TEACHING_HOSPITAL, ehf, latitude , longitude , OnComplete=OnComplete )        

    def Add_Placements(self, placements):
        super().Add_Placements(placements)

        if self.Completed():                      
            # Add placements          
            if self.current_day.day == 2 :            
                if "Medical" not in placements :
                    placements["Medical"] = {}
                    placements["Medical"]["count"] = 0
                    placements["Medical"]["placed"] = 0         
                
                budget = 250000 
                placements["Medical"]["count"] += budget // 1200                   
                for e in (e for e in self.ehf.e.enrolled 
                        if e.available <= self.current_day                                   
                        and e.specialization == "Advanced_Medical_Training"                                
                    ):
                    if budget > 1200:
                        e.add_placement(self, "Medical_Placement", self.last_day_of_month(self.current_day ))                              
                        placements["Medical"]["placed"] += 1
                        budget -= 1200

                    else:
                        break