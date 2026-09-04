import base64
import numpy as np
from flask import Flask, jsonify, render_template, request

from direction_calculator import calculate_direction, calculate_distance
from path_config import compute_path
from sample_map import MARKER_LOCATIONS, MARKER_FLOORS, TRANSITION_NODES

try:
    import cv2
    import cv2.aruco as aruco
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

app = Flask(__name__)

ARROWS = {
    "LEFT": "←",
    "RIGHT": "→",
    "FORWARD": "↑",
    "BACKWARD": "↓",
    "UPSTAIRS": "⇡",
    "DOWNSTAIRS": "⇣"
}

def build_route(start, destination):
    path = compute_path(start, destination)
    if not path:
        return None

    steps = []
    total_distance = 0.0

    for index, step in enumerate(path):
        marker_id = step["id"]
        floor = MARKER_FLOORS.get(marker_id, 0)
        location_name = MARKER_LOCATIONS.get(marker_id, f"Marker {marker_id}")

        step_data = {
            "step_index": index + 1,
            "marker_id": marker_id,
            "location": location_name,
            "floor": floor,
            "type": step["type"],
            "direction": "FORWARD" if index == 0 else "NONE",
            "arrow": "↑" if index == 0 else "",
            "distance_m": 0,
        }

        if index == 0:
            step_data["instruction"] = f"Start at {location_name} (Floor {floor})"
        else:
            previous_marker = path[index - 1]["id"]
            if step["type"] == "transition":
                transition_info = TRANSITION_NODES.get(marker_id, {})
                t_type = transition_info.get("type", "Stairs/Lift")
                step_data["instruction"] = f"Take {t_type} at {location_name} to change floor"
                step_data["direction"] = "UPSTAIRS" if floor > MARKER_FLOORS.get(previous_marker, 0) else "DOWNSTAIRS"
                step_data["arrow"] = ARROWS.get(step_data["direction"], "↕")
            else:
                direction = calculate_direction(previous_marker, marker_id)
                distance = calculate_distance(previous_marker, marker_id)
                total_distance += distance
                step_data["direction"] = direction
                step_data["distance_m"] = distance
                step_data["arrow"] = ARROWS.get(direction, "↑")
                step_data["instruction"] = (
                    f"Go {direction.lower()} for {distance}m towards {location_name}"
                )

        steps.append(step_data)

    return {
        "start": {
            "id": start,
            "name": MARKER_LOCATIONS[start],
            "floor": MARKER_FLOORS.get(start, 0)
        },
        "destination": {
            "id": destination,
            "name": MARKER_LOCATIONS[destination],
            "floor": MARKER_FLOORS.get(destination, 0)
        },
        "total_distance_m": round(total_distance, 2),
        "total_steps": len(steps),
        "path": path,
        "steps": steps,
    }


@app.get("/")
def index():
    destinations = [
        {
            "id": marker_id,
            "name": name,
            "floor": MARKER_FLOORS.get(marker_id, 0)
        }
        for marker_id, name in sorted(MARKER_LOCATIONS.items(), key=lambda item: (MARKER_FLOORS.get(item[0], 0), item[1]))
    ]
    return render_template("index.html", destinations=destinations)


@app.get("/api/destinations")
def destinations():
    dest_list = [
        {
            "id": marker_id,
            "name": name,
            "floor": MARKER_FLOORS.get(marker_id, 0),
            "is_transition": marker_id in TRANSITION_NODES
        }
        for marker_id, name in sorted(MARKER_LOCATIONS.items(), key=lambda item: (MARKER_FLOORS.get(item[0], 0), item[1]))
    ]
    return jsonify(dest_list)


@app.post("/api/route")
def route():
    payload = request.get_json(silent=True) or request.form

    try:
        start = int(payload.get("start"))
        destination = int(payload.get("destination"))
    except (TypeError, ValueError):
        return jsonify({"error": "start and destination must be valid marker IDs"}), 400

    if start not in MARKER_LOCATIONS or destination not in MARKER_LOCATIONS:
        return jsonify({"error": "Unknown marker ID"}), 400

    route_data = build_route(start, destination)
    if route_data is None:
        return jsonify({"error": "No route found for the selected markers"}), 404

    return jsonify(route_data)


@app.post("/api/detect_marker")
def detect_marker():
    if not OPENCV_AVAILABLE:
        return jsonify({"error": "OpenCV not available on server"}), 501

    payload = request.get_json(silent=True) or {}
    image_b64 = payload.get("image")
    if not image_b64:
        return jsonify({"error": "No image data provided"}), 400

    try:
        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]
        img_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(gray)

        detected_markers = []
        if ids is not None:
            for i, marker_id in enumerate(ids):
                m_id = int(marker_id[0])
                location = MARKER_LOCATIONS.get(m_id, f"Unknown Marker {m_id}")
                floor = MARKER_FLOORS.get(m_id, 0)
                detected_markers.append({
                    "id": m_id,
                    "location": location,
                    "floor": floor
                })

        return jsonify({"markers": detected_markers, "count": len(detected_markers)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

