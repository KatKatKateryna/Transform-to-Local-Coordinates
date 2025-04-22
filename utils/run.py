
from typing import Any, Dict

from datetime import datetime, timezone
from speckle_automate import AutomationContext
from specklepy.objects.base import Base
from specklepy.logging.exceptions import SpeckleException
from specklepy.api import operations
from specklepy.core.api.wrapper import StreamWrapper
from specklepy.core.api.client import SpeckleClient
from specklepy.logging.metrics import set_host_app
from specklepy.transports.server import ServerTransport

from main import FunctionInputs


def load_speckle_data(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs) -> Dict:
    
    """Receive and process Speckle data, return geojson."""
    version_root_object = automate_context.receive_version()

    speckle_data = traverse_data(commit_obj, comments)
    
    set_actions(self, client, "GEO post-receive")

    speckle_data["features"].extend(speckle_data["comments"])
    speckle_data["comments"] = []

    speckle_data["project_id"] = wrapper.stream_id
    speckle_data["project"] = stream['name']
    speckle_data["model"] = branch['name']
    speckle_data["model_last_version_date"] = datetime.strptime(commit['createdAt'].replace("T", " ").replace("Z","").split(".")[0], '%Y-%m-%d %H:%M:%S')
    speckle_data["model_id"] = wrapper.model_id
    speckle_data["extent"] = self.extent
    speckle_data["extent3d"] = self.extent3d
    speckle_data["limit_message"] = self.limit_message

    return speckle_data

def traverse_data(self, commit_obj, comments) -> Dict:
    """Traverse Speckle commit and return geojson with features."""

    # from specklepy.objects.geometry import Point, Line, Curve, Arc, Circle, Ellipse, Polyline, Polycurve, Mesh, Brep
    # from specklepy.objects.GIS.layers import VectorLayer
    from specklepy.objects.data_objects import DataObject
    from specklepy.objects.graph_traversal.traversal import (
        GraphTraversal,
        TraversalRule,
    )
    supported_classes = [DataObject] #Mesh, Brep, Point, Line, Polyline, Curve, Arc, Circle, Ellipse, Polycurve]
    supported_types = [y().speckle_type for y in supported_classes]
    r'''
    supported_types.extend([
        "Objects.Other.Revit.RevitInstance", 
        "Objects.BuiltElements.Revit.RevitWall", 
        "Objects.BuiltElements.Revit.RevitFloor", 
        "Objects.BuiltElements.Revit.RevitStair",
        "Objects.BuiltElements.Revit.RevitColumn",
        "Objects.BuiltElements.Revit.RevitBeam",
        "Objects.BuiltElements.Revit.RevitElement",
        "Objects.BuiltElements.Revit.RevitRebar"])
    '''
    # traverse commit
    data: Dict[str, Any] = {
        "type": "FeatureCollection",
        "features": [],
        "comments": [],
        "extent": [-180,-90,180,90],
        "model_crs": "-",
    }

    # rule to keep traversing the object's "x" attribute "item" (both conditions need to be fulfilled)
    # 1. if the item type is not in supported (convertible) types or is GIS VectorLayer
    # 2. if the item's value is a list or a GH object 
    rule = TraversalRule(
        [lambda _: True],
        lambda x: [
            item
            for item in x.get_member_names()
            if (x.speckle_type.split(":")[-1] not in supported_types or isinstance(x, VectorLayer))
            and (isinstance(getattr(x, item, None), list) or (self.sourceApp is not None and "grasshopper" in self.sourceApp.lower() and x.speckle_type == "Base") )
        ],
    )

    # for the context list, save the displayable objects and Layers (for getting CRS for now)
    context_list = [x for x in GraphTraversal([rule]).traverse(commit_obj) if isDisplayable(x.current) or x.current.speckle_type.endswith("VectorLayer")]

    get_set_crs_settings(self, commit_obj, context_list, data)

    set_default_color(context_list)
    self.material_color_proxies: dict = get_material_color_proxies(commit_obj)

    create_features(self, context_list, comments, data)

    # sort features by height 
    
    #if len(data['features']) == len(data['heights']):
    #feat_array = np.array(data['features'])
    #heights_array = np.array(data['heights'])
    #inds = heights_array.argsort()
    #sorted = feat_array[inds].tolist()
    time1 = datetime.now()
    sorted_list = sorted(data['features'], key=lambda d: d['max_height'])
    for i, _ in enumerate(sorted_list):
        sorted_list[i]["properties"]["FID"] = i+1 
    data['features'] = sorted_list
    time2 = datetime.now()
    
    time_operation = (time2-time1).total_seconds()
    self.times["time_sort"] = time_operation
    # print(f"Sorting time: {time_operation}")

    return data
