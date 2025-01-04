from assets import AssetType
from EducationalFacilities import EducationalFacilities

class engineering_school(EducationalFacilities):
    def __init__(self, ehf , latitude , longitude, OnComplete=None):
        super().__init__( AssetType.ENGINEERING_SCHOOL, ehf, latitude , longitude , OnComplete=OnComplete )

        