from flask import Flask, jsonify
from configparser import SafeConfigParser
from os import environ, path

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
    APP_PORT = environ.get("APP_PORT")

app = Flask(__name__)


@app.route("/api/v1/api1")
def api1():
    json_response = {
        "role": role,
        "variable1": var1,
        "variable2": var2,
        "variable3": var3,
    }
    return jsonify(json_response)


@app.route("/api/v1/api2")
def api2():
    pass


@app.route("/")
@app.route("/dashboard")
def dashboard():
    pass


@app.route("/health")
def health():
    return jsonify({"status": "up", "health": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7700)
