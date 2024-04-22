from flask import Flask, jsonify, request
from configparser import SafeConfigParser
from os import environ, path, system
from sys import argv, stdout
import logging
from requests import get

logging.basicConfig(
    filename="pykad_app.log",
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

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

if "VARIABLE2" in environ:
    var2 = environ.get("VARIABLE2")
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
    print(svc_name, svc_param)
    if svc_param and svc_name:
        # https://www.google.com/search?q=kubernetes
        # svc_url = f"http://{svc_name}/api/v1/api1/{svc_param}"
        svc_url = f"https://www.{svc_name}.com/search?q={svc_param}"
        print(svc_url)
        response = get(
            svc_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
            },
        )
        return response.text


@app.route("/api/v1/env")
def show_env():
    env_vars = system("set")
    return f"<p>{env_vars}</p>"


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
