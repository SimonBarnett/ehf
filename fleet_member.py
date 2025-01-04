
from datetime import date, timedelta
import random

class FleetMember:
    def __init__(self, registration_date):
        """
        Initialize a FleetMember with a name and registration date.

        :param name: Name of the fleet member
        :param registration_date: Date of registration, defaults to today's date if not provided
        """        
        self.registration_date = registration_date 
        self.courses_attended = []
        self.available = registration_date
        self.year = 1
        self.specialization = None

    def matriculate(self):
        """
        Matriculate the fleet member for the next year.
        """
        self.year += 1
    
    def meets_requirements(self,prerequisites):
        """
        Check if the fleet member meets the prerequisites for a course.

        :param prerequisites: List of courses that must be completed before taking the course
        :return: True if all prerequisites are met, False otherwise
        """
        for course in prerequisites:
            if course not in self.courses_attended:
                return False
        return True

    def add_course(self, course_name, completion_date=None):
        """
        Add a course that the fleet member has attended.

        :param course_name: Name of the course attended
        :param completion_date: Date when the course was completed, defaults to today if not provided
        """
        self.available = completion_date        
        self.courses_attended.append(course_name)

    def add_placement(self, asset, placement_name, completion_date=None):
        """
        Add a placement that the fleet member has attended.

        :param placement_name: Name of the placement attended
        :param completion_date: Date when the placement was completed, defaults to today if not provided
        """
        count = 0
        self.available = completion_date        
        for c in self.courses_attended:
            if c.startswith(placement_name):
                count = int(c.split(placement_name)[1])
                self.courses_attended.remove(f"{c}")
                break
                
        self.courses_attended.append(f"{placement_name}{count+1}")

    def __str__(self):
        """
        String representation of the FleetMember.

        :return: A string describing the fleet member including registration details and courses attended
        """
        course = ", ".join(self.courses_attended)
        return (f"[{course}]")

class enlistment():

    def __init__(self,day:date):
        self.enrolled = []        
        self.current_day = day
        self.start = False

    def set_current_day(self, day: date):
        """
        Advance the simulation to the given day.

        :param day: The date to advance the simulation to
        """
        for i in range((day - self.current_day).days):                              
            self.current_day += timedelta(days=1)
            
            if self.start and self.current_day.month == 8 and self.current_day.day == 31:
                for student in self.enrolled:
                    student.matriculate()                        
                    
                self.enrolled = [student for student in self.enrolled if student.year <= 4]
                
            if self.start and self.current_day.month == 9 and self.current_day.day == 1:
                self.model_ehf_applications(0.8, 770000, 1.2)    

    def model_ehf_applications(self , uk_tertiary_takeup_rate, total_uk_population_18, ehf_appeal_factor=1.0):

        """
        Model the number of applications to EHF University based on UK tertiary education trends.

        :param year: The year for which we're modeling applications
        :param uk_tertiary_takeup_rate: The percentage of 18-year-olds in the UK entering tertiary education as a float (0.0 to 1.0)
        :param total_uk_population_18: The number of 18-year-olds in the UK for the given year
        :param ehf_appeal_factor: A multiplier to adjust for EHF's unique appeal or reputation, default is 1.0 (no adjustment)
        :return: An estimate of applications to EHF University
        """
        # Calculate total UK tertiary education applicants
        uk_tertiary_applicants = int(total_uk_population_18 * uk_tertiary_takeup_rate)
        
        # Assume EHF gets a fraction of these applications based on its appeal
        # This is a very simple model, you might want to include more factors like:
        # - EHF's capacity relative to other universities
        # - Specific program offerings
        # - Geographic location or international appeal
        ehf_applications = int(uk_tertiary_applicants * 0.01 * ehf_appeal_factor)  # Assuming EHF captures 1% of the market, adjusted by appeal

        # Add some variability to the model for realism
        variability = random.uniform(0.9, 1.1)  # 10% variability either way
        ehf_applications = int(ehf_applications * variability)

        # Model applications to EHF University
        for e in range(ehf_applications):
            self.enrolled.append(FleetMember(self.current_day))        
    
    def __str__(self):
        c = 0    
        str = ""
        for yr in (yr for yr in range(1,5) if any(student.year == yr for student in self.enrolled)):
            course_counts = {}
            str += f"\nYear {yr}"

            for student in (student for student in self.enrolled if student.courses_attended and student.year == yr):
                c += 1
                courses_str = ", ".join(sorted(student.courses_attended))
                
                if courses_str in course_counts:
                    course_counts[courses_str]["count"] += 1
                else:
                    course_counts[courses_str] = {"str": courses_str, "count": 1}
        
            # Print courses with their count
            for courses in course_counts.values():
                str += f"\n\t{courses['str']} - {courses['count']} students"

        str += f"\nTrained {c} of {len(self.enrolled)}\n" 
        return str