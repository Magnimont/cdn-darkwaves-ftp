from flask import request, jsonify, send_file
from services import save_and_check_file, insert_file_metadata, get_file_metadata
from utils import error_handler, serve_video_with_player
import uuid
import os

def configure_routes(app, db, upload_directory):

    @app.route('/upload', methods=['POST'])
    def upload_file():
        files = request.files
        if not files:
            return error_handler("No files were uploaded", 404)

        uploaded_file = files.get('file')
        if not uploaded_file:
            return error_handler("No file was uploaded", 404)

        file_id = str(uuid.uuid4())
        filename = file_id + uploaded_file.filename
        if not filename:
            return error_handler("File Name Not Provided", 404)

        file_extension = os.path.splitext(filename)[1].lower()
        is_image = file_extension in ['.jpg', '.jpeg', '.png', '.gif']
        file_path = os.path.join(upload_directory, filename)

        # Check if it's an image or video
        if is_image:
            content_status = save_and_check_file(uploaded_file, file_path, is_image)
            if isinstance(content_status, tuple):  # Error handler returned
                return content_status
        else:
            uploaded_file.save(file_path)
            content_status = {"isAdultContent": False}

        # Store file metadata in MongoDB
        file_metadata = {
            '_id': file_id,
            'filename': filename,
            'path': file_path,
            'content_type': 'image' if is_image else 'video',
            'adult_content': content_status.get("isAdultContent", False)
        }
        insert_file_metadata(db, file_metadata)
        return jsonify(file_metadata)

    @app.route('/files/<file_id>', methods=['GET'])
    def get_file_path(file_id):
        file_metadata = get_file_metadata(db, file_id)
        if file_metadata:
            return jsonify({'path': f'/get/{file_id}'})
        else:
            return error_handler("file not found", 404)

    @app.route('/get/<file_id>', methods=['GET'])
    def get_file(file_id):
        file_metadata = get_file_metadata(db, file_id)
        if not file_metadata:
            return error_handler("File not found", 404)

        file_path = file_metadata['path']
        content_type = file_metadata['content_type']

        if content_type == 'video':
            return serve_video_with_player(file_id, file_path)
        else:
            return send_file(file_path, as_attachment=False)
