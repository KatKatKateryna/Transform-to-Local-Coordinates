
from pyproj import CRS


def create_crs_from_wkt(wkt: str) -> CRS:
    """Create and assign CRS object from WKT string."""

    return CRS.from_user_input(wkt)

    
def create_custom_crs(lat: float, lon: float) -> CRS:
    """Create and assign custom CRS using Lat & Lon."""

    wkt = f'PROJCS["SpeckleCRS_latlon_{lat}_{lon}", GEOGCS["GCS_WGS_1984", DATUM["D_WGS_1984", SPHEROID["WGS_1984", 6378137.0, 298.257223563]], PRIMEM["Greenwich", 0.0], UNIT["Degree", 0.0174532925199433]], PROJECTION["Transverse_Mercator"], PARAMETER["False_Easting", 0.0], PARAMETER["False_Northing", 0.0], PARAMETER["Central_Meridian", {lon}], PARAMETER["Scale_Factor", 1.0], PARAMETER["Latitude_Of_Origin", {lat}], UNIT["Meter", 1.0]]'
    crs_obj = CRS.from_user_input(wkt)
    return crs_obj
    

def create_crs_from_authid(authid: str ) -> CRS:
    """Create and assign CRS object from Authority ID."""

    crs_obj = CRS.from_string(authid)
    return crs_obj
