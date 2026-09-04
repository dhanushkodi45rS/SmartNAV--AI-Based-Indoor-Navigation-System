# path_config.py

from .graph_map import GRAPH
from .a_star import a_star
from .sample_map import TRANSITION_NODES

# Marker IDs
START = 0
KITCHEN = 1
BEDROOM = 2
BALCONY = 3
BATHROOM = 4
STAIRS = 5
TERRACE1 = 6
TERRACE2 = 7

# Define your journey
START_MARKER = 0       # Start/Entrance
DEST_MARKER = 6        # Terrace 1

def compute_path(start, destination):
    """
    Compute structured path from start to destination using A*.
    Returns list of path steps with type information.
    """
    # A* computes the numeric path
    numeric_path = a_star(GRAPH, start, destination)
    
    if not numeric_path:
        print(" No path found!")
        return []
    
    # Convert to structured path
    structured_path = []
    for marker_id in numeric_path:
        if marker_id in TRANSITION_NODES:
            # This is a stair/elevator
            structured_path.append({
                "type": "transition", 
                "id": marker_id, 
                "action": "UP"
            })
        else:
            # Regular waypoint
            structured_path.append({
                "type": "node", 
                "id": marker_id
            })
    
    return structured_path

# Initial path computation (optional - can also start empty)
PATH = compute_path(START_MARKER, DEST_MARKER)
print(" Initial Computed Path:", PATH)

