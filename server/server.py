from flask import Flask, Response, stream_with_context, request, send_from_directory
from flask_cors import CORS
import json
import os

from main import love_in_paradise

# Configure Flask to serve the /out folder
app = Flask(__name__, static_folder="../out", static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Serve frontend
@app.route("/")
def serve_index():
    """Serve the main index.html"""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    """Serve static assets (JS, CSS, images)"""
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        # For SPA routing, serve index.html if file doesn't exist
        return send_from_directory(app.static_folder, "index.html")

# API endpoint
@app.route("/api/home", methods=["GET", "POST"])
def handle_post_request():
    data = request.get_json()
    if data:
        name = data.get("name")
        return Response(
            stream_with_context(
                json.dumps(result) + "\n"
                for result in love_in_paradise(name)
            ),
            mimetype="application/x-ndjson",
        )
    else:
        return "Invalid request", 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)