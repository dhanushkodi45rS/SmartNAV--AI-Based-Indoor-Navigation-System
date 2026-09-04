import cv2
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)


aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejected = detector.detectMarkers(frame)

    
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        print("Detected marker IDs:", ids.flatten())

    
    cv2.imshow('ArUco Marker Detection - MGRNav', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
