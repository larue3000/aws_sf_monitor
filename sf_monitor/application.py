from flask import Flask, request, jsonify
from flask_cors import CORS
from monitor import get_status


app = Flask(__name__)
CORS(app)


@app.route("/restricted/get_status", methods=["POST"])
def restricted_get_status():
    content = request.json
    return jsonify(get_status(content['arn']))

