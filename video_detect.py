from nudenet import NudeDetector
from better_profanity import profanity
import cv2
import os

classifier = NudeDetector()


def check_video(video_path: str) -> dict:
    def check_Nude_Content(detections, threshold=0.1):
        exposed_parts = [
            "FEMALE_BREAST_EXPOSED",
            "MALE_GENITALIA_EXPOSED",
            "FEMALE_GENITALIA_EXPOSED",
            "BUTTOCKS_EXPOSED",
            "ANUS_EXPOSED",
            "FEET_EXPOSED",
        ]
        for detection in detections:
            if detection['class'] in exposed_parts and detection['score'] > threshold:
                return True
        return False

    if not video_path or not os.path.exists(video_path):
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False

    isNudeContent = False
    isAdultContent = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to an image file-like object
        _, buffer = cv2.imencode('.jpg', frame)
        frame_path = 'frame.jpg'
        with open(frame_path, 'wb') as f:
            f.write(buffer)

        # Check the frame using the nude detector
        prop = classifier.detect(frame_path)
        if check_Nude_Content(prop):
            isNudeContent = True
            break

        # Remove the temporary frame file
        os.remove(frame_path)

    cap.release()

    return {"isNudeContent": isNudeContent, "isAdultContent": isAdultContent}

# Example usage:
# video_status = check_video("path_to_video.mp4")
# print(video_status)
