from pymongo import MongoClient
import os
from utils import error_handler, check_image, check_video

def save_and_check_file(file, file_path, is_image=True):
    file.save(file_path)
    if is_image:
        image_status = check_image(file_path)
        if not image_status:
            return error_handler("File check error", 404)
        elif image_status["isNudeContent"]:
            os.remove(file_path)
            return error_handler("File contains nude content", 404)
        return image_status
    else:
        video_status = check_video(file_path)
        if not video_status:
            return error_handler("File check error", 404)
        elif video_status["isNudeContent"]:
            os.remove(file_path)
            return error_handler("File contains nude content", 404)
        return video_status

def insert_file_metadata(db, file_metadata):
    collection = db['files']
    collection.insert_one(file_metadata)

def get_file_metadata(db, file_id):
    collection = db['files']
    return collection.find_one({'_id': file_id})
