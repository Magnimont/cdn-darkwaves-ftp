import os


def check_video(video_path: str) -> dict:

    if not video_path or not os.path.exists(video_path):
        return False

    isNudeContent = False
    isAdultContent = False


    return {"isNudeContent": isNudeContent, "isAdultContent": isAdultContent}

# Example usage:
# video_status = check_video("path_to_video.mp4")
# print(video_status)
