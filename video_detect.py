import cv2
import os


def check_video(video_path: str) -> dict:

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


        # Remove the temporary frame file
        os.remove(frame_path)

    cap.release()

    return {"isNudeContent": isNudeContent, "isAdultContent": isAdultContent}

# Example usage:
# video_status = check_video("path_to_video.mp4")
# print(video_status)
