from typing import List
import logging

from flask import Flask, request, jsonify
from flask import Response as FlaskResponse
from flask_cors import CORS

from db import Database

import config

log = config.log

app = Flask(__name__)
cors = CORS(app, origins="*")

db = Database(config.DB_CONNECT_STR)


@app.route("/putNewPattern/", methods=["POST"])
def add_new_device():
    data = request.json
    try:
        db.add_pattern(data.get("pattern", None))
    except ValueError:
        return FlaskResponse(
            "Invalid formatted data provided for pattern", status=406
        )

    return FlaskResponse("added pattern to db", status=201)


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
    db.add_device(data.get("device", {}))

    return FlaskResponse("added to db", status=201)


@app.route("/updateDevice/", methods=["POST"])
def update_existing_device() -> FlaskResponse:
    """Updates an existing device in the database

    Returns:
        FlaskResponse: Message and HTTP Status code
    """
    data = request.json
    try:
        db.update_device(data.get("device", None))
    except ValueError as e:
        log.exception(e)
        return FlaskResponse("Device wasn't received", status=406)

    return FlaskResponse("Added to db", status=201)


@app.route("/deleteDevice/", methods=["POST"])
def delete_device():
    data = request.json
    log.info(data)
    db.delete_device(data.get("device", {}))

    return FlaskResponse("Deleted from db", status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6843)
