from flask import Flask, jsonify
from flask_cors import CORS
from main import love_in_paradise
from flask import request

def favorite_food():
    return("cheesecake")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/home", methods=['GET', 'POST'])

#POST

def handle_post_request():
  data = request.get_json()
  if data:
    name = data.get('name')
    # return jsonify({"message": f"Hello, {name}!",
    #                 }), 200
    return jsonify({
       'message': f"ALL NEWS: \n {love_in_paradise(name)}"
    })

  else:
     return jsonify({"error": "Invalid request"}), 400


#GET
# def return_home():
#     return jsonify({
#         # 'message': love_in_paradise(),
#         'favorite_dog' : favorite_food()
#     })
    

    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)#remove when release




