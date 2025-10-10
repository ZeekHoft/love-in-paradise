from flask import Flask, Response, stream_with_context
from flask_cors import CORS
from flask import request
import json

from main import love_in_paradise


def favorite_food():
    return "cheesecake"


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# POST
@app.route("/api/home", methods=["GET", "POST"])
def handle_post_request():
    data = request.get_json()
    if data:
        name = data.get("name")
        return Response(
            stream_with_context(
                # Convert to string ending with newline
                json.dumps(result) + "\n"
                for result in love_in_paradise(name)
            ),
            mimetype="application/x-ndjson",
        )
    else:
        return "Invalid request", 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
