# graph_map.py

MARKER_COORDS = {
    0: (0, 0, 3),       #SunJava
    1: (3.5, 0 , 3),    #Department Entrance
    2: (6, 2.5, 3),     #Lift 3
    3: (3.5, -3, 3),    #Staff Cabin
    4: (2.5, -2, 3),    #HOD Room
    5: (3, -2.5, 3),    #Dept Office
    6: (2, 0 , 2),      #Digital Resource Centre(DRC)
    7: (6, 2.5, 2),     #Lift 2
    8: (6, 2.5, 1),     #Lift 1
    9: (6, 2.5, 0),     #Lift 0
    10: (3.5, 4, 3),    #Stairs Third Floor
    11: (3.5, 4, 0),    #Stairs Ground Floor
    12: (6, 1, 2),      #Internet Lab
    13: (-1, 11, 0),    #Admission Office
    14: (5, 11, 0),     #Register Office
    15: (-1, 11, 2),    #Controller Of Examination Office
    16: (5, 11, 2),     #Computing and Research Lab(CAR Lab)
    17: (-1, 11, 1),    #Dept of ECE
    18: (-1, 1, 1),     #Dept of AIDS
    19: (6, 1, 1),      #Dept of CSE
    20: (-1, 1, 0)      #Chancellor Room
}

GRAPH = {
    0: [(1, 3.5), (2, 6.5), (10, 4)],            # Sunjava → Dept Entrance, Lift
    1: [(0, 3.5), (2, 3), (3, 3), (4, 2), (5, 2.5)],  # Dept Entrance → all
    2: [(0, 6.5), (1, 3)],  # Lift ↔ Sunjava, Dept Entrance
    3
    : [(1, 3), (4, 2), (5, 2)],                       # Staff Cabin → Dept Entrance
    4: [(1, 2), (3, 2), (5, 1)],                       # HOD Room → Dept Entrance
    5: [(1, 2.5), (3, 2), (4, 1)],                       # Dept Office → Dept Entrance
    6: [(7, 5.5), (12, 3), (15, 12), (16, 13)],                       # R&D → Lift (only way up)
    7: [(6, 5.5), (15, 15), (16, 7)],                       # Lift → R&D
    8: [(17, 3), (18, 6), (19, 6)],                       # Lift → Depts ECE, AIDS, CSE
    9: [(13, 15), (14, 7), (20, 6)],
    10:[(0, 4), (2, 3), (1, 4), (11, 35)],                       # Stairs Third Floor → Sunjava, Lift, Dept Entrance, Stairs Ground Floor
    11:[(10, 35), (9, 3), (13, 11), (14, 9)],                       # Stairs Ground Floor → Stairs Third Floor, Lift, Admission Office, Register Office
    12:[(6, 3), (15, 15), (16, 10)],
    13:[(9, 15), (11, 11), (14, 6), (20, 10)],
    14:[(9, 7), (11, 9), (13, 6), (15, 13), (16, 13)],
    15:[(6, 12), (7, 15), (12, 15), (14, 13)],
    16:[(6, 13), (7, 7), (12, 10), (14, 13)],
    17:[(8, 15), (18, 10), (19, 17)],
    18:[(17, 6), (8, 6)],
    19:[(17, 17), (8, 6)],
    20:[(9, 10), (11, 4),(13, 10)]
}