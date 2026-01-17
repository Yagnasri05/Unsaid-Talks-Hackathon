import cv2
import mediapipe as mp
import numpy as np

def get_face_centers(video_path):
    """
    Analyzes the video and returns a list of face center (x) coordinates for each frame.
    If no face is found, returns the previous center or center of the frame.
    """
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(video_path)
    centers = []
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    last_center = width // 2
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)
        
        current_center = last_center

        if results.detections:
            for detection in results.detections:
                # bounding_box = detection.location_data.relative_bounding_box
                # We prioritize the first face found for simplicity, or the largest.
                # MediaPipe returns relative coordinates (0-1).
                bbox = detection.location_data.relative_bounding_box
                center_x = bbox.xmin + bbox.width / 2
                current_center = int(center_x * width)
                break # Just take the first face
        
        centers.append(current_center)
        last_center = current_center

    cap.release()
    return centers

def smooth_centers(centers, window_size=30):
    """
    Smooths the center coordinates using a moving average.
    """
    if not centers:
        return []
        
    smoothed = np.convolve(centers, np.ones(window_size)/window_size, mode='same')
    
    # Handle edges properly (convolve leaves 0s or low values at edges with 'same' sometimes depending on implementation)
    # A simple moving average is better manual implementation for preserving length
    
    smoothed_list = []
    for i in range(len(centers)):
        start = max(0, i - window_size // 2)
        end = min(len(centers), i + window_size // 2)
        window = centers[start:end]
        avg = sum(window) / len(window)
        smoothed_list.append(int(avg))
        
    return smoothed_list
