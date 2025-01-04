from enum import Enum
import random
import json
from datetime import date, timedelta , datetime
from dateutil.relativedelta import relativedelta
import math

class ShipType(Enum):
    FRIGATE = "FRIGATE"
    HOSPITAL_SHIP = "HOSPITAL_SHIP"
    ENGINEERING_BARGE = "ENGINEERING_BARGE"
    FLEET_TRANSPORT = "FLEET_TRANSPORT"
    RAPID_RESPONSE_HELICOPTER = "RAPID_RESPONSE_HELICOPTER"
    UTILITY_BOAT = "UTILITY_BOAT"
    RIB = "RIB"
    DIVING_SUPPORT_VESSEL = "DIVING_SUPPORT_VESSEL"
    DRONE_SWARM = "DRONE_SWARM"
    MEDIVAC_HELICOPTER = "MEDIVAC_HELICOPTER"

class ShipStatus(Enum):
    UNDER_CONSTRUCTION = "Under Construction"
    IN_TRANSIT = "In Transit"
    PORT_SIDE = "Port Side"
    DEPLOYED = "Deployed"
    MAINTENANCE = "Maintenance"
    OVERHAUL = "Overhaul"
    RETIRED = "Retired"

class Ship:
    SHIP_PROPERTIES = {}
    BASE_SALARIES = {
        'naval': 30000,
        'force_protection': 35000,
        'medical': 40000,
        'engineering': 38000,
        'it': 45000,
        'catering': 25000
    }

    #region Constructors
    @classmethod
    def load_properties(cls):
        if not cls.SHIP_PROPERTIES:
            with open('ships.json', 'r') as f:
                cls.SHIP_PROPERTIES = json.load(f)

    def __init__(self, ship_type: ShipType, construction_start_date: date = None, latitude: float = None, longitude: float = None):
        """
        Initialize a Ship object with properties loaded from JSON based on the ship type.

        :param ship_type: The type of the ship as an Enum value
        :param construction_start_date: The date when construction of the ship starts, defaults to today's date if not provided
        :param latitude: The current latitude of the ship (in degrees)
        :param longitude: The current longitude of the ship (in degrees)
        """
        self.load_properties()  # Load properties if not already loaded
        properties = self.SHIP_PROPERTIES.get(ship_type.name)
        if properties is None:
            raise ValueError(f"Unknown ship type: {ship_type}")

        self.type = ship_type
        self.status = ShipStatus.UNDER_CONSTRUCTION
        self.current_day = construction_start_date        
        self.cost_price = properties['cost_price']
        self.build_time = properties['build_time']
        self.maintenance = properties['maintenance']
        self.overhaul = properties['overhaul']
        self.expected_lifetime = properties['expected_lifetime']
        self.name = random.choice(properties['names'])  # Select a random name from the list
        self.crew = properties['crew']  # Adding crew details
        self.running_costs = properties['running_costs']  # Adding running costs
        self.parent = None

        if not 'upgrades' in properties:
            self.daily_sailing_distance = properties['daily_sailing_distance']  # Adding daily sailing distance      
            self.isupgrade = False
        else:
            self.upgradesVessel = properties['upgrades']
            self.isupgrade = True

        # Calculate launch date based on build time
        start_date = construction_start_date 
        build_time_months = self._parse_build_time(self.build_time)
        self.launch_date = self._add_months(start_date, build_time_months)

        # Set initial position
        self.latitude = latitude if latitude is not None else 0.0  # Default to 0.0 if not provided
        self.longitude = longitude if longitude is not None else 0.0  # Default to 0.0 if not provided
        self.destination_latitude = latitude if latitude is not None else 0.0  # Default to 0.0 if not provided
        self.destination_longitude = longitude if longitude is not None else 0.0  # Default to 0.0 if not provided
        
        # Maintenance and overhaul locations
        self.last_serviced = self.launch_date
        self.last_overhaul = self.launch_date
        self.maintenance_location = self.maintenance['location']
        self.overhaul_location = self.overhaul['location']
        self.days_to_next_maintenance = (self.get_next_maintenance() - self.current_day).days
        self.days_to_next_overhaul = (self.get_next_overhaul() - self.current_day).days

        self.upgrades = []  # List of upgrades applied to the ship
    
    #endregion Constructors

#region Parse times and frequencies   
     
    def _parse_build_time(self, build_time_str):
        """
        Parse the build time string into months.

        :param build_time_str: String representation of build time, e.g., "48 months", "2 years"
        :return: Number of months as an integer
        """
        parts = build_time_str.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid build time format: {build_time_str}")
        
        quantity = int(parts[0])
        unit = parts[1].lower()

        if unit.startswith('month'):
            return quantity
        elif unit.startswith('year'):
            return quantity * 12
        else:
            raise ValueError(f"Unrecognized time unit: {unit}")

    def _parse_frequency(self, frequency_str):
        """
        Parse the frequency string to determine the time between events.

        :param frequency_str: String representation of frequency, e.g., "Annual", "Every 5 years"
        :return: Tuple of (quantity, unit)
        """
        parts = frequency_str.split()
        if len(parts) == 1:  # Annual
            return 1, 'year'
        elif len(parts) == 3:
            return int(parts[1]), parts[2].rstrip('s')  # Remove 's' from plural forms
        else:
            raise ValueError(f"Unrecognized frequency format: {frequency_str}")

    def _add_months(self, source_date, months):
        """
        Add months to the given date, accounting for different month lengths.

        :param source_date: The original date
        :param months: Number of months to add
        :return: New date after adding months
        """
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return date(year, month, day)

    def next_scheduled_event(self, event_type, event, last_event_date):
        """
        Calculate the next scheduled event (maintenance or overhaul) based on the last event date and current date.

        :param event_type: String description of the event, either 'maintenance' or 'overhaul'
        :param event: Dictionary containing 'frequency' key
        :param last_event_date: Date of the last event
        :return: Next scheduled date for the event
        """
        frequency, unit = self._parse_frequency(event['frequency'])
 
        if unit == 'year':
            next_date = last_event_date + timedelta(days=frequency * 365)
        elif unit == 'month':
            next_date = last_event_date + timedelta(days=frequency * 30)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")

        return next_date

    #endregion Parse times and frequencies        

    def __str__(self):
        if self.status == ShipStatus.UNDER_CONSTRUCTION:
            years, months = self.get_years_months_till_launch()
            formatted_cost = "£{:,.2f}".format(self.cost_price)
            return (f"\n{self.name} ({self.type.value}) - {self.status.value} \n\tBuild Cost: {formatted_cost} - "
                f"Build Time: {self.build_time} - "                
                f"\n\tLaunch Date: {self.launch_date} - {years} years and {months} months"
                )
        elif self.status == ShipStatus.RETIRED:
            return f"\n{self.name} ({self.type.value}) - {self.status.value}"
        
        else:
            years, months = self.get_age()
            formatted_cost = "£{:,.0f}".format(self.calculate_total_running_costs())            
            
            upgrades_str = ""
            if len(self.upgrades) > 0:
                upgrades_str = "\n" + ('Upgrades: ' + ', '.join(str(upgrade) for upgrade in self.upgrades)).replace('\n', '\n\t')
            
            req = (' - '.join(f"{name}: £{value:,.0f}" for name, value in self.ShipRequirements().items())).replace('\n', '\n\t')
            
            stat = ""
            pos = ''
            if self.isupgrade:
                if self.parent == None:
                    stat = self.status.value                    
                    pos = '\n\t' + f"Position: Latitude {self.latitude}, Longitude {self.longitude}"

                else:
                    stat = self.parent.name                                                

            else:
                pos = '\n\t' + f"Position: Latitude {self.latitude}, Longitude {self.longitude}"
                stat = self.status.value

            crew = ('Crew: ' + ' - '.join(f"{role}: {count}" for role, count in self.shipCrew().items() if count > 0)).replace('\n', '\n\t')
            crew_wages = "{:,.0f}".format(self.total_wages())
            
            return (f"\n{self.name} ({self.type.value}) - {stat} "
                f"\n\t{crew}"
                f"\n\tRunning Cost: {formatted_cost} : "                    
                f"Crew: £ {crew_wages} - {req}  "                                       
                f"\n\tAge: {years} years and {months} months / {self.expected_lifetime} years : "                                    
                f"Last Service: {self.last_serviced}, Next: {self.days_to_next_maintenance} days : "
                f"Last Overhaul: {self.last_overhaul}, Next: {self.days_to_next_overhaul} days"
                f"{pos}" 
                f"\t{upgrades_str}"                

            )

    #region Running Costs        

    def calculate_total_running_costs(self):
        """
        Calculate the total running costs excluding maintenance, and overhaul.

        :return: Total running costs in GBP per year
        """
        # Add running costs for the ship if launched AND not retired
        if self.current_day > self.launch_date and not self.status == ShipStatus.RETIRED:
            return self.total_wages()  + sum(self.running_costs.values())
        else:
            return 0
        
    def total_wages(self):
        total_wages = 0
        if self.current_day > self.launch_date and not self.status == ShipStatus.RETIRED:
            for role, count in self.crew.items():
                if role in self.BASE_SALARIES:
                    total_wages += count * self.BASE_SALARIES[role]
        
            for upgrade in self.upgrades:            
                total_wages += upgrade.total_wages()

        return total_wages
    
    def ShipRequirements(self):
        req = {}
        for i in self.running_costs:
            if i not in req: 
                req[i] = self.running_costs[i]
            else: 
                req[i] += self.running_costs[i]
    
        for upgrade in self.upgrades:
            for i in upgrade.running_costs:
                if i not in req: 
                    req[i] = upgrade.running_costs[i]
                else: 
                    req[i] += upgrade.running_costs[i]
    
        return req
    
    def shipCrew(self):
        crew = {}
        for i in self.crew:
            if i not in crew: 
                crew[i] = self.crew[i]
            else: 
                crew[i] += self.crew[i]
    
        for upgrade in self.upgrades:
            for i in upgrade.crew:
                if i not in crew: 
                    crew[i] = upgrade.crew[i]
                else: 
                    crew[i] += upgrade.crew[i]
    
        return crew
    
    #endregion Running Costs

    #region Ship Movement
    def set_destination(self, latitude: float, longitude: float):
        """
        Set the destination for the ship.

        :param latitude: The latitude of the destination in degrees
        :param longitude: The longitude of the destination in degrees
        """
        self.destination_latitude = latitude
        self.destination_longitude = longitude

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on Earth.

        :param lat1, lon1: Latitude and longitude of the first point in degrees
        :param lat2, lon2: Latitude and longitude of the second point in degrees
        :return: Distance in nautical miles
        """
        R = 3443.92  # Radius of earth in nautical miles
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def _calculate_bearing(self, lat1, lon1, lat2, lon2):
        """
        Calculate the bearing from one point to another on Earth.

        :param lat1, lon1: Latitude and longitude of the starting point in degrees
        :param lat2, lon2: Latitude and longitude of the destination point in degrees
        :return: Bearing in degrees
        """
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        y = math.sin(lon2 - lon1) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
        bearing = math.degrees(math.atan2(y, x))
        return (bearing + 360) % 360  # Normalize to 0° - 360°

    def move_towards_destination(self):
        """
        Move the ship towards the destination by the daily sailing distance if a destination is set.

        Adjusts the ship's latitude and longitude based on one day's travel.
        """
        if self.destination_latitude is None or self.destination_longitude is None:
            return  # No destination set, no movement

        current_distance = self._calculate_distance(self.latitude, self.longitude, 
                                                    self.destination_latitude, self.destination_longitude)
        if current_distance <= self.daily_sailing_distance:
            # If the distance to the destination is less than or equal to one day's travel, set the ship at the destination
            self.latitude = self.destination_latitude
            self.longitude = self.destination_longitude
            return

        bearing = self._calculate_bearing(self.latitude, self.longitude, 
                                          self.destination_latitude, self.destination_longitude)

        # Convert bearing to radians
        bearing_rad = math.radians(bearing)

        # Calculate the new position
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        d = self.daily_sailing_distance / 3443.92  # Convert nautical miles to radians using Earth's radius

        new_lat = math.asin(math.sin(lat1) * math.cos(d) + 
                            math.cos(lat1) * math.sin(d) * math.cos(bearing_rad))
        new_lon = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(d) * math.cos(lat1),
                                    math.cos(d) - math.sin(lat1) * math.sin(new_lat))

        # Convert back to degrees
        self.latitude = math.degrees(new_lat)
        self.longitude = (math.degrees(new_lon) + 540) % 360 - 180  # Normalize to -180° to +180°

    #endregion Ship Movement

    #region Maintenance and Overhaul

    def get_next_maintenance(self):
        """
        Calculate the date of the next scheduled maintenance.

        :return: The date of the next maintenance
        """
        return self.next_scheduled_event("maintenance", self.maintenance, self.last_serviced)

    def get_next_overhaul(self):
        """
        Calculate the date of the next scheduled overhaul.

        :return: The date of the next overhaul
        """
        return self.next_scheduled_event("overhaul", self.overhaul, self.last_overhaul)

    def service_maintenance(self):
        """
        Update the last serviced date when maintenance is performed.

        :param service_date: The date when maintenance was performed
        """
        self.last_serviced = self.current_day
        self.days_to_next_maintenance = (self.get_next_maintenance() - self.current_day).days        

    def service_overhaul(self):
        """
        Update the last overhaul date when an overhaul is performed.

        :param service_date: The date when the overhaul was performed
        """
        self.last_overhaul = self.current_day
        self.days_to_next_overhaul = (self.get_next_overhaul() - self.current_day).days

    def get_age(self):
        delta = relativedelta(self.current_day, self.launch_date)
        return delta.years, delta.months
    
    def get_years_months_till_launch(self):
        if self.current_day >= self.launch_date:
            return 0, 0  # Already launched
        delta = relativedelta(self.launch_date, self.current_day)
        return delta.years, delta.months
        
#endregion Maintenance and Overhaul

    def set_current_day(self, day: date):
        """
        Set the current day for the ship and calculate daily running costs.

        :param day: The date to set as the current day
        :return: Daily running cost in GBP
        """
        if day < self.current_day :
            raise ValueError(f"Day cannot be set to a previous date: {day}")
        else:
            self.current_day = day    

        if self.status == ShipStatus.UNDER_CONSTRUCTION:
            if self.current_day >= self.launch_date:
                self.status = ShipStatus.PORT_SIDE

        # Check if the ship has reached its expected lifetime
        years, _ = self.get_age()
        if self.status == ShipStatus.PORT_SIDE and years > self.expected_lifetime:
            self.status = ShipStatus.RETIRED

        # Remove any upgrades 
        for upgrade in self.upgrades:
            if self.status == ShipStatus.RETIRED:
                upgrade.status = ShipStatus.PORT_SIDE
                upgrade.latitude = self.latitude
                upgrade.longitude = self.longitude
                upgrade.parent = None

            else:
                upgrade.set_current_day(day)
                upgrade.latitude = self.latitude
                upgrade.longitude = self.longitude

        self.days_to_next_maintenance = (self.get_next_maintenance() - self.current_day).days                
        self.days_to_next_overhaul = (self.get_next_overhaul()-self.current_day).days

        daily_cost = self.calculate_total_running_costs() / 365          
        return daily_cost
    
    def upgrade(self, additional_ship):
        """
        Upgrade the ship with another vessel.

        :param additional_ship_type: The type of the additional ship as an Enum value
        """     
        if self.current_day < self.launch_date:           
            raise ValueError(f"Cannot upgrade before completion: {self.launch_date}")
        
        if self.current_day < additional_ship.launch_date:           
            raise ValueError(f"Cannot upgrade with future vessel: {additional_ship.launch_date}")
        
        if additional_ship.upgradesVessel is None:
            raise ValueError(f"{additional_ship.type} is not an upgrade")
        
        if self.type.name in additional_ship.upgradesVessel:
            additional_ship.parent = self
            self.upgrades.append(additional_ship)
        else:
            raise ValueError(f"Upgrade not compatible with ship type: {additional_ship.type}")

from datetime import date

def test():
    cost = 0
    print(">")
    hopital_ship = Ship(ShipType.HOSPITAL_SHIP, construction_start_date=date(2020, 1, 1), latitude=51.5074, longitude=-0.1278)  # Position near London

    cost += hopital_ship.set_current_day(date(2021, 1, 1))
    print(hopital_ship)

    cost += hopital_ship.set_current_day(date(2022, 1, 1))
    medivac_helicopter = Ship(ShipType.MEDIVAC_HELICOPTER, 
                            construction_start_date=date(2022, 1, 1), 
                            latitude=51.5074, 
                            longitude=-0.1278)  # Position near London
    print(medivac_helicopter)
    rib  = Ship(ShipType.RIB, construction_start_date=date(2022, 1, 1), latitude=51.5074, longitude=-0.1278)  # Position near London

    cost += rib.set_current_day(date(2023, 1, 1))
    cost += hopital_ship.set_current_day(date(2023, 1, 1))
    cost += medivac_helicopter.set_current_day(date(2023, 1, 1))

    hopital_ship.upgrade(medivac_helicopter)
    hopital_ship.upgrade(rib)
    print(hopital_ship)

    cost += hopital_ship.set_current_day(date(2026, 3, 1))
    print(hopital_ship)

    hopital_ship.service_maintenance()
    print(hopital_ship)