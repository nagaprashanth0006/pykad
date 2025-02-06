from flask import Flask, jsonify, request
import configparser
import os
import redis
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Redis connection settings (using Kubernetes DNS)
redis_host = os.getenv("REDIS_HOST", "redis-service.default.svc.cluster.local")
redis_port = int(os.getenv("REDIS_PORT", 6379))

# Attempt to connect to Redis
try:
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, db=0, decode_responses=True
    )
    redis_client.ping()  # Test connection
    logger.info("Connected to Redis successfully.")
except redis.ConnectionError:
    redis_client = None
    logger.warning("Could not connect to Redis. Falling back to no-cache mode.")

# Load configuration from config.ini if it exists
config = configparser.ConfigParser()
config_file = "config.ini"
if os.path.exists(config_file):
    config.read(config_file)
    logger.info("Config file loaded.")

# Read environment variables
env_vars = {key: os.getenv(key) for key in os.environ.keys()}


# Combine config and env vars into a single dictionary
def get_all_vars():
    all_vars = {}
    if "config" in config:
        all_vars.update(config["config"])
    all_vars.update(env_vars)
    return all_vars


# Populate the cache at startup
def populate_cache():
    if redis_client:
        all_vars = get_all_vars()
        for key, value in all_vars.items():
            redis_client.set(key, value)
        logger.info("Cache populated at startup.")
    else:
        logger.warning("Cache not populated because Redis is unavailable.")


populate_cache()


@app.route("/")
def index():
    if redis_client:
        all_vars = {key: redis_client.get(key) for key in redis_client.keys("*")}
        logger.info("Retrieved all variables from cache.")
    else:
        all_vars = get_all_vars()
        logger.warning("Redis unavailable. Retrieved all variables without cache.")
    return jsonify(all_vars)


@app.route("/get", defaults={"var_name": None})
@app.route("/get/<var_name>")
def get_var(var_name):
    if var_name:
        if redis_client:
            value = redis_client.get(var_name)
            if value:
                logger.info(f"Retrieved {var_name} from cache.")
                return jsonify({var_name: value})
            else:
                logger.warning(f"{var_name} not found in cache. Returning N/A.")
                return jsonify({var_name: "N/A"})
        else:
            all_vars = get_all_vars()
            value = all_vars.get(var_name, "N/A")
            logger.warning(f"Redis unavailable. Retrieved {var_name} directly.")
            return jsonify({var_name: value})
    else:
        if redis_client:
            all_vars = {key: redis_client.get(key) for key in redis_client.keys("*")}
            logger.info("Retrieved all variables from cache.")
        else:
            all_vars = get_all_vars()
            logger.warning("Redis unavailable. Retrieved all variables without cache.")
        return jsonify(all_vars)


@app.route("/health")
def health():
    logger.info("Health check.")
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    logger.info("Starting Nimbus application...")
    app.run(host="0.0.0.0", port=3000, debug=True)
