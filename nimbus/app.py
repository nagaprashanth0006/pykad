from flask import Flask, jsonify, request
import configparser
import os
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Load configuration from config.ini if it exists
config = configparser.ConfigParser()
config_file = 'config.ini'
if os.path.exists(config_file):
    config.read(config_file)

# Read environment variables
env_vars = {key: os.getenv(key) for key in os.environ.keys()}

# Combine config and env vars into a single dictionary
def get_all_vars():
    all_vars = {}
    if config_file in config:
        all_vars.update(config[config_file])
    all_vars.update(env_vars)
    return all_vars

@app.route('/')
@cache.cached(timeout=50)
def index():
    return jsonify(get_all_vars())

@app.route('/get')
@cache.cached(timeout=50)
def get_var():
    var_name = request.args.get('var')
    all_vars = get_all_vars()
    if var_name in all_vars:
        return jsonify({var_name: all_vars[var_name]})
    else:
        return jsonify({'error': 'Variable not found'}), 404

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
