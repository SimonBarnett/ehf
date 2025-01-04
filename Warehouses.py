from assets import Asset, AssetType

class Warehouses(Asset):
    def __init__(self):
        super().__init__(asset_type=AssetType.WAREHOUSES)
        self.m3 = self.asset_data.get("m3", 0)  # Default to 0 if not found
        self.upgrades = []
        
    def specific_attributes(self):
        return f"Capacity: {self.m3} m³"

# Create an instance of Warehouses
warehouse = Warehouses()

# Create an instance of WarehouseUpgrade
warehouse_upg = Asset(AssetType.WAREHOUSE_UPGRADE)

# Print details to verify
print(warehouse)
print(warehouse.specific_attributes())
print(warehouse_upg)
