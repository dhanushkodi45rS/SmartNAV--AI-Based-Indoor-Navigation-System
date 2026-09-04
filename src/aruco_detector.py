import cv2
import cv2.aruco as aruco

import tkinter as tk
from threading import Thread
from sample_map import MARKER_LOCATIONS, TRANSITION_NODES
from direction_calculator import calculate_direction, calculate_distance
from path_config import compute_path
from graph_map import GRAPH
from gui_navigation import NavigationGUI

ARROWS = {
    "LEFT": "<--",
    "RIGHT": "-->",
    "FORWARD": "^^",
    "BACKWARD": "vv",
    "UPSTAIRS": "↑↑",
    "DOWNSTAIRS": "↓↓"
}

def marker_area(corner):
    pts = corner[0]
    return cv2.contourArea(pts)

def estimate_distance(area):
    K = 2000
    if area <= 0:
        return None
    return round(K / (area ** 0.5), 2)

# Global variables
current_node = None
AREA_THRESHOLD = 8000 
current_path_index = 0
navigation_completed = False
current_distance = None
PATH = []
rerouting = False
path_calculated = False
gui_app = None

def draw_arrow(frame, direction):
    h, w, _ = frame.shape
    center = (w // 2, h // 2)

    if direction == "FORWARD":
        end = (center[0], center[1] - 100)
    elif direction == "BACKWARD":
        end = (center[0], center[1] + 100)
    elif direction == "LEFT":
        end = (center[0] - 100, center[1])
    elif direction == "RIGHT":
        end = (center[0] + 100, center[1])
    elif direction == "UPSTAIRS":
        end = (center[0], center[1] - 100)
    elif direction == "DOWNSTAIRS":
        end = (center[0], center[1] + 100)
    else:
        return

    cv2.arrowedLine(frame, center, end, (0, 255, 0), 6)

def camera_loop():
    global current_node, current_path_index, navigation_completed
    global current_distance, PATH, rerouting, path_calculated, gui_app
    
    cap = cv2.VideoCapture(0)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    
    print(" Camera started. Use GUI to select destination.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)

        # Only process if navigation started in GUI
        if gui_app and gui_app.is_started():
            goal = gui_app.get_destination()
            
            if ids is not None:
                for i, marker_id in enumerate(ids):
                    detected = int(marker_id[0])
                    area = marker_area(corners[i])
                    
                    # Initialize PATH on first detection
                    if not path_calculated and detected in GRAPH:
                        PATH = compute_path(detected, goal)
                        path_calculated = True
                        print(f" Starting from: {MARKER_LOCATIONS[detected]}")
                        print(f" Path: {[step['id'] for step in PATH]}")
                        
                        # Update GUI on main thread
                        if gui_app:
                            gui_app.root.after(0, lambda: gui_app.update_status(
                                f" Route calculated!\n Starting from: {MARKER_LOCATIONS[detected]}",
                                "#2ecc71"
                            ))
                    
                    # Update distance
                    if current_path_index < len(PATH):
                        expected_step = PATH[current_path_index]
                        expected_marker = expected_step["id"]
                        
                        if detected == expected_marker:
                            current_distance = estimate_distance(area)
                    
                    if area > AREA_THRESHOLD:
                        if current_path_index < len(PATH):
                            expected_step = PATH[current_path_index]
                            expected_marker = expected_step["id"]
                            
                            if detected == expected_marker:
                                current_node = detected
                                rerouting = False
                                
                                if expected_step["type"] == "transition":
                                    print(f"↕ Reached: {MARKER_LOCATIONS[detected]}")
                                else:
                                    print(f"✓ Reached: {MARKER_LOCATIONS[detected]}")
                                
                                if detected == goal:
                                    navigation_completed = True
                                    print(" Destination reached!")
                                    
                                    # Update GUI
                                    if gui_app:
                                        gui_app.root.after(0, gui_app.show_completion)
                                        
                                elif current_path_index < len(PATH) - 1:
                                    current_path_index += 1
                                    next_step = PATH[current_path_index]
                                    print(f"→ Next: {MARKER_LOCATIONS[next_step['id']]}")
                            
                            else:
                                # Re-routing
                                if detected in GRAPH and detected != goal:
                                    print(f" Wrong turn! At: {MARKER_LOCATIONS[detected]}")
                                    
                                    # Update GUI
                                    if gui_app:
                                        gui_app.root.after(0, gui_app.show_rerouting)
                                    
                                    PATH = compute_path(detected, goal)
                                    current_path_index = 0
                                    current_node = detected
                                    rerouting = True
                                    path_calculated = True
                                    
                                    if PATH and current_path_index < len(PATH) - 1:
                                        current_path_index += 1

        # Display navigation
        if current_node is not None and not navigation_completed:
            current = current_node

            if current in MARKER_LOCATIONS:
                location = MARKER_LOCATIONS[current]
                cv2.putText(frame, f"Location: {location}",
                        (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
                if gui_app:
                    gui_app.root.after(0, lambda loc=location: 
                        gui_app.update_status(f" Current Location: {loc}", "#3498db"))
                
                if rerouting:
                    cv2.putText(frame, "Recalculating...",
                            (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 165, 255), 2)
                
                if current_path_index < len(PATH):
                    prev_step = PATH[current_path_index - 1] if current_path_index > 0 else None
                    next_step = PATH[current_path_index]
    
                    if prev_step is not None:
                        # Check if next step is a transition
                        if next_step["type"] == "transition":
                            instruction = "↕ Go upstairs"
                            cv2.putText(frame, instruction,
                                    (30, 120),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 165, 255), 2)
            
                            # Update GUI
                            if gui_app:
                                def update_trans():
                                    gui_app.update_instruction(instruction)
                                gui_app.root.after(0, update_trans)
                
                        else:
                            # Regular navigation
                            prev_node = prev_step["id"]
                            next_node = next_step["id"]
                            direction = calculate_direction(prev_node, next_node)
                            real_distance = calculate_distance(prev_node, next_node)

                            next_location = MARKER_LOCATIONS[next_node]
                            arrow = ARROWS.get(direction, "→")

                            draw_arrow(frame, direction)

                            distance_text = f" for {real_distance}m"
                            instruction_text = f"{arrow} Go {direction}{distance_text} to {next_location}"
            
                            cv2.putText(frame, instruction_text,
                                    (30, 120),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2)
            
                            # Update GUI with proper function
                            if gui_app:
                                gui_instruction = f"{arrow} Go {direction} to {next_location}"
                
                                def update_gui_now():
                                    gui_app.update_instruction(gui_instruction, real_distance)
                
                                gui_app.root.after(0, update_gui_now)
                            
        if navigation_completed:
            cv2.putText(frame, "Destination Reached!",
                (30, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                (0, 0, 255), 3)

        cv2.imshow("MGRNav - Camera View", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    global gui_app
    
    # Create GUI
    root = tk.Tk()
    gui_app = NavigationGUI(root)
    
    # Start camera in separate thread
    camera_thread = Thread(target=camera_loop, daemon=True)
    camera_thread.start()
    
    # Run GUI
    root.mainloop()

if __name__ == "__main__":
    main()