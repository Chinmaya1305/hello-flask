from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({
        "message": "Hello, DevOps — deployed with Jenkins, Docker, Kubernetes and Ansible!",
        "env": {
            "FLASK_ENV": os.environ.get("FLASK_ENV", "production")
        }
    })

@app.route("/health")
def health():
    return jsonify({"status":"ok"}), 200

if __name__ == "__main__":
    # listen on new requested port 4600
    app.run(host="0.0.0.0", port=4600)

