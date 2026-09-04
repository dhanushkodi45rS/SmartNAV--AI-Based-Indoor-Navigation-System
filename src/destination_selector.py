# destination_selector.py

AVAILABLE_DESTINATIONS = {
    0: "Sunjava",
    1: "Dept Entrance",
    2: "3rd Lift",
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

def select_destination():
    print("\nAvailable Destinations:")
    
    for marker_id, name in AVAILABLE_DESTINATIONS.items():
        print(f"{marker_id} -> {name}")
    
    goal = int(input("\nEnter destination marker ID: "))
    
    if goal in AVAILABLE_DESTINATIONS:
        print(f"\nDestination selected: {AVAILABLE_DESTINATIONS[goal]}")
        return goal
    else:
        print("Invalid selection")
        return None
