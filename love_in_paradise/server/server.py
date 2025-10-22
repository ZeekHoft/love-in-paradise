from flask import Flask, Response, stream_with_context, request
from flask_cors import CORS
import json
from main import love_in_paradise

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/home", methods=["POST"])
def handle_post_request():
    data = request.get_json()
    if not data:
        return "Invalid request", 400

    name = data.get("name")
    use_llm = data.get("useLLM", False)
    print(f"Received request: name={name}, useLLM={use_llm}")

    def generate():
        for result in love_in_paradise(name, use_llm=use_llm):
            # Each dict is converted to a single JSON line
            yield json.dumps(result) + "\n"

    return Response(
        stream_with_context(generate()),
        mimetype="application/x-ndjson",
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
