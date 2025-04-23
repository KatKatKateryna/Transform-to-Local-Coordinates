
from pyproj import Transformer
from specklepy.objects.base import Base

from utils.coords_utils import reproject_display_data_list
from utils.crs_utils import create_crs_from_wkt, create_custom_crs
from utils.display_utils import is_displayable, is_primitive

def traverse_transform_data(commit_obj, function_inputs: "FunctionInputs") -> Base:
    """Traverse Speckle data and transform its coordinates."""

    wkt: str = commit_obj.crs["wkt"]
    crs_from = create_crs_from_wkt(wkt)
    crs_to = create_custom_crs(function_inputs.lat, function_inputs.lon)
    
    commit_obj["crs"] = {"wkt":crs_to.to_wkt(), "unit":"Meters","authid":"","description":f"SpeckleCRS_latlon_{function_inputs.lat}_{function_inputs.lon}"}
    transformer = Transformer.from_crs(
        crs_from,
        crs_to,
        always_xy=True,
    )

    layers = commit_obj.elements
    for layer in layers:
        for feature in layer.elements: # each feature is a QgisObject (DataObject)

            for displayData in feature["displayValue"]:

                display_list = []
                # don't change Table items - only displayable objects
                if is_displayable(displayData):
                    if is_primitive(displayData):
                        display_list = [displayData]
                        reproject_display_data_list(display_list, transformer)
                    else: # Region, Brep
                        display_list = displayData.displayValue
                        reproject_display_data_list(display_list, transformer)

