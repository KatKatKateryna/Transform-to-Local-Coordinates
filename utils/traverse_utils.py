
from specklepy.objects.base import Base

from utils.coords_utils import reproject_display_data_list
from utils.crs_utils import create_crs_from_wkt, create_custom_crs
from utils.display_utils import is_displayable, is_primitive

def traverse_transform_data(commit_obj, function_inputs: "FunctionInputs") -> Base:
    """Traverse Speckle data and transform it's coordinates."""

    wkt: str = commit_obj.crs.wkt
    crs_from = create_crs_from_wkt(wkt)
    crs_to = create_custom_crs(function_inputs.lat, function_inputs.lon)

    layers = commit_obj.elements
    for layer in layers:
        for feature in layer.elements: # each feature is a QgisObject (DataObject)

            for displayData in feature.displayValue:

                display_list = []
                if is_displayable(displayData):
                    if is_primitive(displayData):
                        display_list = [displayData]
                        reproject_display_data_list(display_list, crs_from, crs_to)
                    else:
                        display_list = displayData.displayValue
                        reproject_display_data_list(display_list, crs_from, crs_to)

