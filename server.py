from typing import List
import logging

from flask import Flask, request, jsonify
from flask import Response as FlaskResponse
from flask_cors import CORS

from db import Database

import config

log = config.log

app = Flask(__name__)
# cors = CORS(app, origins=config.secrets["CORS_ALLOWED_DOMAINS"])
cors = CORS(app, origins='*')

db = Database(config.secrets.get("db_url"))

@app.route("/getDevices/", methods=["GET"])
def get_devices():
    response_dict = {}
    devices = db.get_all_devices()
    for i, device in enumerate(devices):
        response_dict[str(i)] = device.get_dict()

    return jsonify(response_dict)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6843)
