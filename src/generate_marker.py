import cv2
import cv2.aruco as aruco
import os

# Create output folder for markers
output_folder = "../markers"
os.makedirs(output_folder, exist_ok=True)

# Select a predefined dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Marker size (in pixels)
marker_size = 300

# Generate and save  markers
for marker_id in range(25):
    marker_image = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    file_path = os.path.join(output_folder, f"marker_{marker_id}.png")
    cv2.imwrite(file_path, marker_image)
    print(f" Generated: {file_path}")

print("\n  ArUco markers created successfully in the 'markers' folder!")
