# direction_map.py

# Edge-based direction mapping
# Format: (from_node, to_node): direction
# This maps the physical direction you need to turn/walk

DIRECTION_MAP = {
    # From Start (0)
    (0, 1): "FORWARD",   # Start → Kitchen
    (1, 0): "BACKWARD",   # Kitchen → Start (turn around)

    # From Kitchen (1)
    (1, 2): "LEFT",      # Kitchen → Bedroom
    (2, 1): "RIGHT",     # Bedroom → Kitchen

    # From Bedroom (2)
    (2, 3): "FORWARD",     # Bedroom → Balcony
    (3, 2): "BACKWARD",      # Balcony → Bedroom
    
    (2, 4): "RIGHT",   # Bedroom → Bathroom
    (4, 2): "LEFT",   # Bathroom → Bedroom

    (0,5): "LEFT",    # Start → Stairs
    (5,0): "RIGHT",   # Stairs → Start

    (5,6): "LEFT",   # Stairs → Terrace 1
    (6,5): "RIGHT",  # Terrace 1 → Stairs

    (5,7): "RIGHT",  # Stairs → Terrace 2
    (7,5): "LEFT"   # Terrace 2 → Stairs

    # Add more as needed...
}