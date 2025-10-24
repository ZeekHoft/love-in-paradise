from flask import (
    Flask,
    Response,
    stream_with_context,
    request,
    send_from_directory,
    redirect,
)
from flask_cors import CORS
import json
import os
import sys
from main import love_in_paradise

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/home", methods=["POST"])
def handle_post_request():
    try:
        data = request.get_json()
        if not data:
            return "Invalid request", 400

        name = data.get("name")
        use_llm = data.get("useLLM", False)

        print(
            f"Received request from {request.remote_addr}: name={name}, useLLM={use_llm}"
        )
        sys.stdout.flush()

        def generate():
            try:
                for result in love_in_paradise(name, use_llm=use_llm):
                    # Use NDJSON format (newline-delimited JSON)
                    json_line = json.dumps(result) + "\n"
                    yield json_line
                    sys.stdout.flush()
            except Exception as e:
                # Send error as final line
                print(f"Error in generate: {e}")
                import traceback

                traceback.print_exc()

                error_result = {
                    "verdict": None,
                    "justification": f"Server error: {str(e)}",
                    "confidence": None,
                    "sources": [],
                    "currentProcess": "Error",
                    "progress": 1.0,
                }
                yield json.dumps(error_result) + "\n"

        return Response(
            stream_with_context(generate()),
            mimetype="application/x-ndjson",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )
    except Exception as e:
        print(f"API Error: {e}")
        import traceback

        traceback.print_exc()
        return {"error": str(e)}, 500


# Redirect root to home.html
@app.route("/")
def index():
    return redirect("/home.html")


# Handle routes without .html extension
@app.route("/home")
def home_redirect():
    return redirect("/home.html")


@app.route("/about")
def about_redirect():
    return redirect("/about.html")


@app.route("/help")
def help_redirect():
    return redirect("/help.html")


# Serve static files from 'out' directory
@app.route("/<path:path>")
def serve_static(path):
    # Check if file exists in out directory
    file_path = os.path.join("out", path)
    if os.path.exists(file_path):
        return send_from_directory("out", path)

    # Try adding .html extension
    html_path = os.path.join("out", f"{path}.html")
    if os.path.exists(html_path):
        return send_from_directory("out", f"{path}.html")

    # If path doesn't exist, try serving home.html (for client-side routing)
    return send_from_directory("out", "home.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
