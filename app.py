
import os
from flask import Flask, jsonify, render_template
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "dev")

REQUESTS = Counter(
    "smartdeploy_http_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)


@app.route("/")
def home():
    REQUESTS.labels(endpoint="/").inc()
    return render_template("index.html", version=VERSION)


@app.route("/health")
def health():
    return jsonify(
        status="healthy",
        version=VERSION
    ), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


@app.route("/ready")
def ready():
    return jsonify(status="ready"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
