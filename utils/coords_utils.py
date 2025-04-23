
import copy
import math
from typing import List
from pyproj import CRS, Transformer

from specklepy.objects.base import Base
from specklepy.objects.geometry import Point, Polyline, Mesh


def reproject_display_data_list(base_obj_list: List[Base], crs_from: CRS, crs_to: CRS)-> List[List[float]]:
    for item in base_obj_list:
        if isinstance(item, Point):
            coords = [[item.x, item.y, item.z]]
            new_coords = reproject_2d_coords_list(coords, crs_from, crs_to)
            item.x = new_coords[0][0]
            item.y = new_coords[0][1]
            item.z = new_coords[0][2]

        elif isinstance(item, Polyline):
            coords = []
            for i in range(int(len(item.value)/3)):
                coords.append([item.value[i*3], item.value[i*3+1], item.value[i*3+2]])
            new_coords = reproject_2d_coords_list(coords, crs_from, crs_to)
            item.value = new_coords	

        elif isinstance(item, Mesh):
            coords = []
            for i in range(int(len(item.vertices)/3)):
                coords.append([item.vertices[i*3], item.vertices[i*3+1], item.vertices[i*3+2]])	

            new_coords = reproject_2d_coords_list(coords, crs_from, crs_to)
            item.vertices = new_coords


def reproject_2d_coords_list(coords_in: List[List[float]], crs_from: CRS, crs_to: CRS) -> List[List[float]]:
    """Return coordinates in a CRS of SpeckleProvider."""

    transformer = Transformer.from_crs(
        crs_from,
        crs_to,
        always_xy=True,
    )
    transformed = [[pt[0], pt[1], pt[2]] for pt in transformer.itransform(copy.deepcopy(coords_in))]
        
    return transformed
