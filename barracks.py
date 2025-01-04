from assets import AssetType
from EducationalFacilities import EducationalFacilities

class barracks(EducationalFacilities):
    def __init__(self, ehf , latitude , longitude, OnComplete=None):
        super().__init__( AssetType.BARRACKS, ehf, latitude , longitude , OnComplete=OnComplete )

        