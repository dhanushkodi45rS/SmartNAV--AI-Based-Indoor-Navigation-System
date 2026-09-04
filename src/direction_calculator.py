# direction_calculator.py

import math
from .graph_map import MARKER_COORDS

def calculate_direction(current_node, next_node):
    """
    Calculate direction based on coordinate difference.
    Returns direction string: FORWARD, LEFT, RIGHT, UPSTAIRS, DOWNSTAIRS
    """
    x1, y1, z1 = MARKER_COORDS[current_node]
    x2, y2, z2 = MARKER_COORDS[next_node]
    
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    
    # Floor change takes priority
    if dz > 0:
        return "UPSTAIRS"
    elif dz < 0:
        return "DOWNSTAIRS"
    
    # Horizontal movement - based on which axis changes more
    if abs(dx) > abs(dy):
        # Primarily left-right movement
        if dx > 0:
            return "RIGHT"
        else:
            return "LEFT"
    else:
        # Primarily forward-backward movement
        if dy > 0:
            return "FORWARD"
        else:
            return "BACKWARD"

def calculate_distance(current_node, next_node):
    """
    Calculate Euclidean distance between two markers.
    """
    x1, y1, z1 = MARKER_COORDS[current_node]
    x2, y2, z2 = MARKER_COORDS[next_node]
    
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    
    return round(math.sqrt(dx**2 + dy**2 + dz**2), 2)