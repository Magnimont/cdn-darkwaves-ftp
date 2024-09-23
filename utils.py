from flask import jsonify, render_template_string, Response
import os
import re

def error_handler(message, code):
    return jsonify({'error': message}), code

def serve_video_with_player(file_id, file_path):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Advanced Video Player</title>
    </head>
    <body>
        <div>
            <video id="videoPlayer" controls>
                <source id="videoSource" src="/stream/{file_id}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div>
            <!-- Skip Controls -->
            <button onclick="skip(-10)">Rewind 10s</button>
            <button onclick="skip(10)">Skip 10s</button>

            <!-- Playback Speed Controls -->
            <label for="speedControl">Playback Speed:</label>
            <select id="speedControl" onchange="setPlaybackSpeed()">
                <option value="0.5">0.5x</option>
                <option value="1" selected>1x (Normal)</option>
                <option value="1.5">1.5x</option>
                <option value="2">2x</option>
            </select>
        </div>

        <script>
            const videoPlayer = document.getElementById('videoPlayer');
            const videoSource = document.getElementById('videoSource');
            const speedControl = document.getElementById('speedControl');

            function skip(seconds) {{ videoPlayer.currentTime += seconds; }}

            function setPlaybackSpeed() {{ videoPlayer.playbackRate = speedControl.value; }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

def send_video_file(file_path, range_header):
    try:
        if not os.path.exists(file_path):
            return error_handler(f"File not found: {file_path}", 404)

        byte1, byte2 = 0, None
        match = re.search(r'(\d+)-(\d*)', range_header)
        if match:
            groups = match.groups()
            if groups[0]:
                byte1 = int(groups[0])
            if groups[1]:
                byte2 = int(groups[1])

        file_size = os.path.getsize(file_path)
        length = file_size - byte1
        if byte2 is not None:
            length = byte2 - byte1 + 1

        with open(file_path, 'rb') as f:
            f.seek(byte1)
            data = f.read(length)

        rv = Response(data,
                      206,
                      mimetype='video/mp4',
                      content_type='video/mp4',
                      direct_passthrough=True)
        rv.headers.add('Content-Range', f'bytes {byte1}-{byte1 + length - 1}/{file_size}')
        rv.headers.add('Accept-Ranges', 'bytes')
        return rv

    except FileNotFoundError:
        return error_handler(f"File not found: {file_path}", 404)
    except PermissionError:
        return error_handler(f"Permission denied: {file_path}", 403)
    except Exception as e:
        return error_handler(f"Error serving video: {str(e)}", 500)
