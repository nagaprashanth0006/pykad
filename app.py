from flask import Flask, jsonify, request
from configparser import SafeConfigParser
from os import environ, path
from sys import argv, stdout
import logging

logging.basicConfig(level=logging.DEBUG, stream=stdout)

"""
1. Initialize variables with "Undefined"
    or any other values within script
2. config.ini file
3. Env variables
4. params to program
"""

params = "None Given"
role = "Undefined"
var1 = "Undefined"
var2 = "Undefined"
var3 = "Undefined"
APP_PORT = 7700

if path.exists("config.ini"):
    configParser = SafeConfigParser()
    configParser.read("config.ini")

    if configParser.has_option("Default", "APP_ROLE"):
        role = configParser.get("Default", "APP_ROLE")

    if configParser.has_option("Default", "VARIABLE_1"):
        var1 = configParser.get("Default", "VARIABLE_1")

    if configParser.has_option("Default", "VARIABLE_2"):
        var2 = configParser.get("Default", "VARIABLE_2")

    if configParser.has_option("Default", "APP_PORT"):
        APP_PORT = configParser.get("Default", "APP_PORT")

if "VARIABLE3" in environ:
    var3 = environ.get("VARIABLE3")
if "APP_PORT" in environ:
    APP_PORT = environ.get("APP_PORT").strip()

if len(argv) > 1:
    params = " ".join(argv[1:])
    for param in params.split(" "):
        if "role=" in param:
            role = param.split("=")[-1].strip()

app = Flask(__name__)


@app.route("/api/v1/api1")
def api1():
    json_response = {
        "role": role,
        "variable1": var1,
        "variable2": var2,
        "variable3": var3,
        "parameters": params,
    }
    return jsonify(json_response)


@app.route("/api/v1/api2")
def api2():
    svc_name = request.args.get("service")
    svc_param = request.args.get("param")
    if svc_param and svc_name:
        svc_url = f"http://{svc_name}/api/v1/api1/{svc_param}"
        response = request.get(svc_url)
        return response.text


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return jsonify({"role": role, "message": "App running"})


@app.route("/health")
def health():
    return jsonify({"status": "up", "health": "healthy"})


if __name__ == "__main__":
    app.logger.info(f"Starting app on port:{APP_PORT}")
    app.run(host="0.0.0.0", port=int(APP_PORT))
