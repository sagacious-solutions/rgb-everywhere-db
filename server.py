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
cors = CORS(app, origins="*")

db = Database(config.secrets.get("db_url"))


@app.route("/getDevices/", methods=["GET"])
def get_devices():
    response_dict = {}
    devices = db.get_all_devices()
    for i, device in enumerate(devices):
        response_dict[str(i)] = device.get_dict()

    return jsonify(response_dict)


@app.route("/putNewDevice/", methods=["POST"])
def add_new_device():
    data = request.json
    log.info(data)
    db.add_device(data.get("device", {}))

    return FlaskResponse("added to db", status=201)


@app.route("/deleteDevice/", methods=["POST"])
def delete_device():
    data = request.json
    log.info(data)
    db.delete_device(data.get("device", {}))

    return FlaskResponse("Deleted from db", status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6843)
