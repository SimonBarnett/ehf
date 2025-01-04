from assets import Asset, AssetType

class Headquarters(Asset):
    def __init__(self):
        super().__init__(asset_type=AssetType.HEADQUARTERS)
        self.number_of_operations_rooms = self.asset_data.get("number_of_operations_rooms", 0)  # Default to 0 if not found
        self.upgrades = []
        
    def specific_attributes(self):
        return f"Number of Operations Rooms: {self.number_of_operations_rooms}"

# Create an instance of Headquarters
hq = Headquarters()

# Create instances of related upgrades
hq_ops_room_upg = Asset(AssetType.OPERATIONS_ROOM_UPGRADE)
hq_planning_staff_upg = Asset(AssetType.PLANNING_STAFF_UPGRADE)

# Print details to verify
print(hq)
print(hq.specific_attributes())
print(hq_ops_room_upg)
print(hq_planning_staff_upg)
