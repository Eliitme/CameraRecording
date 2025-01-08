from flask import Flask, Response, request, send_file
from flask_restful import Resource, Api

import os
import re


app = Flask(__name__)
api = Api(app)

def generate_tree(path):
    tree = {}
    for root, dirs, files in os.walk(path):
        # Get the relative path of the current directory
        rel_path = os.path.relpath(root, path)
        # Split the path into components
        components = rel_path.split(os.sep) if rel_path != '.' else []
        # Navigate to the correct branch in the tree
        current_level = tree
        for comp in components:
            current_level = current_level.setdefault(comp, {})
        # Add files to the current level
        current_level.update({file: None for file in files})
    return tree


class FileTree(Resource):
    def get(self):
        tree = generate_tree('recordings')

        return tree
    

class File(Resource):
    def get(self, path):
        video_path = os.path.join('recordings', path)  # Replace with the path to your video file

    # Check if the file exists
        if not os.path.exists(video_path):
            return "Video not found", 404

        # Support for HTTP range requests
        range_header = request.headers.get('Range', None)
        if range_header:
            range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
            if range_match:
                start = int(range_match.group(1))
                end = range_match.group(2)
                end = int(end) if end else os.stat(video_path).st_size - 1
                chunk_size = (end - start) + 1

                with open(video_path, 'rb') as f:
                    f.seek(start)
                    chunk = f.read(chunk_size)

                response = Response(chunk, 206, mimetype='video/mp4')
                response.headers.add('Content-Range', f'bytes {start}-{end}/{os.stat(video_path).st_size}')
                response.headers.add('Accept-Ranges', 'bytes')
                return response

        # For non-range requests, return the entire file
        return send_file(video_path, mimetype='video/mp4')

api.add_resource(FileTree, '/file-tree') # Route_1
api.add_resource(File, '/recordings/<path:path>') # Route

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
