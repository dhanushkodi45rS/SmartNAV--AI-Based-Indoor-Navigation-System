MARKER_LOCATIONS = {
    0: "Sunjava",
    1: "Dept Entrance",
    2: "Lift",
    3: "Staff Cabin",
    4: "HOD Room",
    5: "Dept Office",
    6: "Digital Resource Centre(DRC)",
    7: "2nd Lift",
    8: "1st Lift",
    9: "Ground Floor Lift",
    10:"Stairs Third Floor",
    11:"Stairs Ground Floor",
    12:"Internet Lab",
    13:"Admission Office",
    14:"Register Office",
    15:"Controller Of Examination Office",
    16:"Computing and Research Lab(CAR Lab)",
    17:"Dept of ECE",
    18:"Dept of AIDS",
    19:"Dept of CSE",
    20:"Chancellor Room"
}

MARKER_FLOORS = {
    0: 3,  # Third floor
    1: 3,  # Third floor
    2: 3,  # Third floor (lift entry)
    3: 3,  # Third floor
    4: 3,  # Third floor
    5: 3,  # Third floor
    6: 2,  # Second floor
    7: 2,  # Second floor (lift entry)
    8: 1,  # First floor (lift entry)
    9: 0,  # Ground floor (lift entry)
    10: 3, # Third floor (stairs entry) 
    11: 0, # Ground floor (stairs entry)
    12: 2, # Second floor
    13: 0, # Ground floor
    14: 0, # Ground floor       
    15: 2, # Second floor
    16: 2, # Second floor
    17: 1, # First floor
    18: 1, # First floor
    19: 1, # First floor
    20: 0  # Ground floor
}

TRANSITION_NODES = {
    2: {"type": "3rd Lift", "connects": [(3, 2), (3, 1), (3, 0)]},  # Lift connects floor 3 to floor 1, floor 2 and floor 0
    7: {"type": "2nd Lift", "connects": [(2, 3), (2, 1), (2, 0)]},  # Lift connects floor 2 to floor 0, floor 1 and floor 3
    8: {"type": "1st Lift", "connects": [(1, 3), (1, 2), (1, 0)]},  # Lift connects floor 1 to floor 0, floor 2 and floor 3
    9: {"type": "Ground Floor Lift", "connects": [(0, 3), (0, 2), (0, 1)]},  # Lift connects floor 0 to floor 3, floor 2 and floor 1
    10: {"type": "Stairs", "connects": [(3, 0)]},  # Stairs connect floor 3 to floor 0
    11: {"type": "Stairs", "connects": [(0, 3)]}   # Stairs connect floor 0 to floor 3
}
