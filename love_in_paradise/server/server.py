

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
    
    name = data.get('name').title()
    return jsonify({
       'message': f"ALL NEWS: \n {love_in_paradise(name)}"
      #  'message': f"ALL NEWS: \n {(name)}"
        
    })
    

  else:
     return jsonify({"error": "Invalid request"}), 400

    

    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)




