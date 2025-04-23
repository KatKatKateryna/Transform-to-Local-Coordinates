
from typing import List

DEFAULT_COLOR = (255 << 24) + (150 << 16) + (150 << 8) + 150


def isDisplayable(obj: "Base") -> bool:

    if is_primitive(obj):
        return True
    
    displayValue = None
    if hasattr(obj, 'displayValue'):
        displayValue = getattr(obj, 'displayValue')
    elif hasattr(obj, '@displayValue'):
        displayValue = getattr(obj, '@displayValue')
    
    # merge to sigle object, if List
    if isinstance(displayValue, List):
        return True
    
    return False


def is_primitive(obj) -> bool:
    """Check if the object can be converted directly."""
    
    from specklepy.objects.geometry import Polyline, Point, Line, Arc, Circle, Curve, Polycurve, Mesh, Brep

    if (
        isinstance(obj, Point) or
        isinstance(obj, Line) or
        isinstance(obj, Polyline) or
        isinstance(obj, Arc) or
        isinstance(obj, Circle) or
        isinstance(obj, Curve) or
        isinstance(obj, Mesh) 
        ):
            return True
    return False
