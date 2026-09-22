
Here's the updated Python code including a new MEDIVAC_HELICOPTER ship type:

python
from enum import Enum

class ShipType(Enum):
    FRIGATE = "Constellation-class Frigate"
    HOSPITAL_SHIP = "Hospital Ship"
    ENGINEERING_BARGE = "Engineering Barge"
    FLEET_TRANSPORT = "Fleet Transport"
    RAPID_RESPONSE_HELICOPTER = "Rapid Response Helicopter"
    UTILITY_BOAT = "Utility Boat"
    RIB = "Rigid Inflatable Boat"
    DIVING_SUPPORT_VESSEL = "Diving Support Vessel"
    DRONE_SWARM = "Drone Swarm"
    MEDIVAC_HELICOPTER = "Medivac Helicopter"

class Ship:
    SHIP_PROPERTIES = {
        ShipType.FRIGATE: {
            "cost_price": 1200000000,
            "build_time": "48 months",
            "maintenance": {"price": 20000000, "frequency": "Annual", "duration": "1 week"},
            "overhaul": {"price": 125000000, "frequency": "Every 5 years", "duration": "6 months"},
            "expected_lifetime": 25
        },
        ShipType.HOSPITAL_SHIP: {
            "cost_price": 850000000,
            "build_time": "36 months",
            "maintenance": {"price": 12500000, "frequency": "Annual", "duration": "10 days"},
            "overhaul": {"price": 75000000, "frequency": "Every 7 years", "duration": "4 months"},
            "expected_lifetime": 30
        },
        ShipType.ENGINEERING_BARGE: {
            "cost_price": 10000000,
            "build_time": "24 months",
            "maintenance": {"price": 1250000, "frequency": "Annual", "duration": "5 days"},
            "overhaul": {"price": 5000000, "frequency": "Every 10 years", "duration": "2 months"},
            "expected_lifetime": 40
        },
        ShipType.FLEET_TRANSPORT: {
            "cost_price": 500000000,
            "build_time": "30 months",
            "maintenance": {"price": 10000000, "frequency": "Annual", "duration": "7 days"},
            "overhaul": {"price": 50000000, "frequency": "Every 6 years", "duration": "3 months"},
            "expected_lifetime": 35
        },
        ShipType.RAPID_RESPONSE_HELICOPTER: {
            "cost_price": 20000000,
            "build_time": "12 months",
            "maintenance": {"price": 10000000, "frequency": "Annual", "duration": "3 days"},
            "overhaul": {"price": 5000000, "frequency": "Every 5 years", "duration": "1 month"},
            "expected_lifetime": 20
        },
        ShipType.UTILITY_BOAT: {
            "cost_price": 1000000,
            "build_time": "6 months",
            "maintenance": {"price": 50000, "frequency": "Annual", "duration": "2 days"},
            "overhaul": {"price": 250000, "frequency": "Every 3 years", "duration": "1 week"},
            "expected_lifetime": 15
        },
        ShipType.RIB: {
            "cost_price": 500000,
            "build_time": "3 months",
            "maintenance": {"price": 25000, "frequency": "Annual", "duration": "1 day"},
            "overhaul": {"price": 100000, "frequency": "Every 2 years", "duration": "3 days"},
            "expected_lifetime": 10
        },
        ShipType.DIVING_SUPPORT_VESSEL: {
            "cost_price": 2000000,
            "build_time": "8 months",
            "maintenance": {"price": 100000, "frequency": "Annual", "duration": "3 days"},
            "overhaul": {"price": 500000, "frequency": "Every 4 years", "duration": "2 weeks"},
            "expected_lifetime": 20
        },
        ShipType.DRONE_SWARM: {
            "cost_price": 5000000,
            "build_time": "6 months",
            "maintenance": {"price": 500000, "frequency": "Annual", "duration": "1 month"},
            "overhaul": {"price": 1000000, "frequency": "Every 3 years", "duration": "2 weeks"},
            "expected_lifetime": 5
        },
        ShipType.MEDIVAC_HELICOPTER: {
            "cost_price": 25000000,
            "build_time": "12 months",
            "maintenance": {"price": 1500000, "frequency": "Annual", "duration": "3 days"},
            "overhaul": {"price": 6000000, "frequency": "Every 5 years", "duration": "1 month"},
            "expected_lifetime": 20
        }
    }

def __init__(self, ship_type: ShipType):
    """
    Initialize a Ship object with properties based on the ship type.

    :param ship_type: The type of the ship as an Enum value
    """
    properties = self.SHIP_PROPERTIES.get(ship_type)
    if properties is None:
        raise ValueError(f"Unknown ship type: {ship_type}")
    
    self.type = ship_type
    self.cost_price = properties['cost_price']
    self.build_time = properties['build_time']
    self.maintenance = properties['maintenance']
    self.overhaul = properties['overhaul']
    self.expected_lifetime = properties['expected_lifetime']

def __str__(self):
    return (f"{self.type.value} - Cost: £{self.cost_price:,} - "
            f"Build Time: {self.build_time} - "
            f"Maintenance: £{self.maintenance['price']:,}/yr, {self.maintenance['frequency']}, {self.maintenance['duration']} - "
            f"Overhaul: £{self.overhaul['price']:,}, {self.overhaul['frequency']}, {self.overhaul['duration']} - "
            f"Expected Lifetime: {self.expected_lifetime} years")

Example usage:
medivac_helicopter = Ship(ShipType.MEDIVAC_HELICOPTER)
print(medivac_helicopter)

frigate = Ship(ShipType.FRIGATE)
print(frigate)

This code now includes the `MEDIVAC_HELICOPTER` with its specific properties. The `Medivac Helicopter` is set with a higher cost than the rapid response helicopter, reflecting specialized medical equipment and capabilities, but with similar maintenance and overhaul schedules due to the nature of helicopter operations.