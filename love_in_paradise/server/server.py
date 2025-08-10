

from flask import Flask, jsonify
from flask_cors import CORS
from main import love_in_paradise


def favorite_food():
    return("cheesecake")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message': love_in_paradise(),
        'favorite_dog' : favorite_food()
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)#remove when release





