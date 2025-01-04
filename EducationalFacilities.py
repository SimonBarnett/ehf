from datetime import date, timedelta
import json
import math
from assets import Asset 

class EducationalFacilities(Asset):    
    def __init__(self, asset_type, ehf , latitude , longitude, OnComplete=None):
        super().__init__(asset_type=asset_type
            , ehf = ehf            
            , latitude=latitude
            , longitude=longitude
            , OnComplete=OnComplete)
        
        self.ehf = ehf
        self.max_classes = self.asset_data["max_classes"]
        self.classes = []
        self.upgrades = []       
        self.admins = 0        
        self.timetable = []

        self.courses = []
        with open('classes.json', 'r') as f:
            data = json.load(f)
            for c in data:
                if self.asset_type.value in data[c].get("provider") :
                    data[c]["class_type"] = c
                    data[c]["wkduration"] = int(data[c].get("class_duration").split(" ")[0])  
                    data[c]["per_year"] = (52 // data[c]["wkduration"])
                    data[c]["places"] = data[c]["per_year"] * data[c]["class_size"] 
                    data[c]["specialization"] = data[c].get("specialization", False) 
                    self.courses.append(data[c])

    def __str__(self):
        if not self.Completed():
            return (f"\n{super().__str__()}")
        
        class_str = ""
        cls = self.all_classes()
        for c in cls:
            class_str += f"\n\t{cls[c]['count']} * {c} ({cls[c]['class_duration']}) Places : {cls[c]['places_yr']}"
        dept_sizes = self.dept_size()
        dept_sizes_str = ', '.join(f"{dept} ({size})" for dept, size in dept_sizes.items())
        return (            
            f"\n{super().__str__()} - Classes: {len(self.classes)} / {self.classrooms():,.0f}  "                                      
            f"{class_str}"  
            f"\nFaculty: {dept_sizes_str}, Admin ({1 + self.admins}) - Wages: £{self.Wages():,.0f}" 
            f"{self.placements_str()}"          
            f"{self.upgrades_str()}"
            f"\nMaintaiance: £{self.facilities_Maintaiance():,.0f}"                
        )
    
    #region Classes

    def classrooms(self):

        c = self.max_classes
        for each in self.Completed_Upgrades():        
            if "max_classes" in each.asset_data:
                c += each.asset_data["max_classes"]

        return c

    def add_class(self, type_name, count=1):
        if not self.Completed:
            raise ValueError(f"{self.asset_type.name} is still being built.")
                
        if not any(c.get("class_type") == type_name for c in self.courses):
            raise ValueError(f"{self.name} does not offer course {type_name}.")
        
        if len(self.classes) < self.classrooms():    
            for i in range(count):
                if len(self.classes) < self.classrooms():
                    self.classes.append(self.courses[[c.get("class_type") for c in self.courses].index(type_name)])
                else:
                    raise ValueError("Maximum number of classes reached.")
        else:
            raise ValueError("Maximum number of classes reached.")        

    def remove_class(self, class_type, count=1):
        removed_count = 0
        for _ in range(count):
            for cls in self.classes:
                if cls["class_type"] == class_type:
                    self.classes.remove(cls)
                    removed_count += 1
                    break
            if removed_count < count:
                raise ValueError(f"Not enough classes of type {class_type.name} to remove.")
        
        self.Make_Faculty()

    def all_classes(self):
        all_classes = {}
        for u in (u for u in self.upgrades if u.Completed()):
            with open('classes.json', 'r') as f:
                data = json.load(f)
                for c in (c for c in data if u.asset_type.value in data[c].get("provider") ):                
                    f = False
                    for cs in self.courses: 
                        if c == cs.get("class_type"): 
                            f = True
                            break
                        
                    if not f:
                        data[c]["class_type"] = c
                        data[c]["wkduration"] = int(data[c].get("class_duration").split(" ")[0])  
                        data[c]["per_year"] = (52 // data[c]["wkduration"])
                        data[c]["places"] = data[c]["per_year"] * data[c]["class_size"] 
                        data[c]["specialization"] = data[c].get("specialization", False) 
                        self.courses.append(data[c])

        for cls in self.courses:
            if cls.get("class_type") not in all_classes:
                all_classes[cls.get("class_type")] = cls
                all_classes[cls.get("class_type")]["count"] = 0
                all_classes[cls["class_type"]]["places_yr"] = all_classes[cls["class_type"]]["places"] * all_classes[cls["class_type"]]["count"]

        for cls in self.classes:
            all_classes[cls.get("class_type")]["count"] += 1 
            all_classes[cls["class_type"]]["places_yr"] = all_classes[cls["class_type"]]["places"] * all_classes[cls["class_type"]]["count"]
            
        return all_classes
    
    def students(self):
        st = 0
        for t in (t for t in self.timetable if t["start_date"] <= self.current_day and t["end_date"] > self.current_day):
            st += t["attendance"] 
        return st + super().students()

    def make_timetable(self):
        timetable = []
        for cls in self.classes:      
            next_start = self.current_day      
            for i in range(cls.get("per_year")+1):
                c = cls.copy()
                c["start_date"] = next_start
                next_start += timedelta(weeks=cls.get("wkduration"))
                c["end_date"] = next_start-timedelta(days=1)
                if not "prerequisites" in c:
                    c["prerequisites"] = []
                c["attendance"] = 0
                timetable.append(c)
        
        self.timetable = timetable

    #endregion
    
    #region Faculty
    def Make_Faculty(self):
        self.employed = []
        if self.Completed():
            self.employed.append(            
                {
                    "role": "Academy Head",
                    "wage": 100000,
                    "count": 1
                })
            self.employed.append(
                {
                    "role": "Department Heads",
                    "wage": 80000,
                    "count": len(self.dept_size())
                })            
            self.employed.append(
                {
                    "role":"Trainers",
                    "wage": 60000,
                    "count": sum(self.dept_size().values()) - 1 
                })     
        
            emp = 0
            for role in self.employed:
                emp += role["count"]
            self.admins = 1 + math.ceil(emp/6)
            self.employed.append(
                {
                    "role":"Admin",
                    "wage": 40000,
                    "count": self.admins
                })      

    def dept_size(self):
        dept_size = {}
        for cls in self.classes:           
            responsible_faculty = cls.get("responsible_faculty", [])
            for dept in responsible_faculty:
                if dept not in dept_size:
                    dept_size[dept] = 0
                dept_size[dept] += 1 / len(responsible_faculty)
        
        for i in dept_size:
            dept_size[i] = math.ceil(dept_size[i])

        return dept_size  
        
    #endregion

    def set_current_day(self, day: date):         
        for i in range((day - self.current_day).days):                  
            super().set_current_day(self.current_day + timedelta(days=1))
            if self.Completed():                
                
                if self.current_day.month == 9 and self.current_day.day == 1:
                    self.Make_Faculty()
                    self.make_timetable()                    

                for c in (c for c in self.timetable if c["start_date"] == self.current_day) : 
                    if c.get("specialization") :
                        for e in (e for e in self.ehf.e.enrolled if e.year > 1 and e.specialization == None): 
                            if e.available <= self.current_day and not c.get("class_type") in e.courses_attended and e.meets_requirements(c.get("prerequisites",[])):                             
                                e.add_course(c.get("class_type"), c.get("end_date"))
                                e.specialization = c.get("class_type")
                                c.update({"class_size": c.get("class_size") - 1})                                 
                                c.update({"attendance": c.get("attendance") + 1})                                 
                            if c.get("class_size") == 0: 
                                break

                    elif len(c["prerequisites"])>0:            
                        for e in (e for e in self.ehf.e.enrolled if e.year > 1 and e.specialization == None): 
                            if e.available <= self.current_day and not c.get("class_type") in e.courses_attended and e.meets_requirements(c.get("prerequisites",[])):                             
                                e.add_course(c.get("class_type"), c.get("end_date"))
                                c.update({"class_size": c.get("class_size") - 1})                                
                                c.update({"attendance": c.get("attendance") + 1})                                 
                            if c.get("class_size") == 0: 
                                break                
                
                    else:
                        for e in (e for e in self.ehf.e.enrolled if e.year == 1 ): 
                            if e.available <= self.current_day and not c.get("class_type") in e.courses_attended and e.meets_requirements(c.get("prerequisites",[])):                             
                                e.add_course(c.get("class_type"), c.get("end_date"))
                                c.update({"class_size": c.get("class_size") - 1})                                
                                c.update({"attendance": c.get("attendance") + 1})                                 
                            if c.get("class_size") == 0: 
                                break                                        