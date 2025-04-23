
from specklepy.objects.geometry import Polyline, Point, Mesh
from typing import List


def is_displayable(obj: "Base") -> bool:

    if is_primitive(obj):
        return True
    
    displayValue = None
    if hasattr(obj, 'displayValue'):
        displayValue = getattr(obj, 'displayValue')
    elif hasattr(obj, '@displayValue'):
        displayValue = getattr(obj, '@displayValue')
    
    if displayValue:
        return True
    
    return False


def is_primitive(obj) -> bool:
    """Check if the object can be converted directly."""
    
    if (
        isinstance(obj, Point) or
        isinstance(obj, Polyline) or
        isinstance(obj, Mesh) 
        ):
            return True
    return False
