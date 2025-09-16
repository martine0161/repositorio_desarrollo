from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    message = os.getenv('MESSAGE', 'Mensaje por defecto')
    release = os.getenv('RELEASE', 'v1')
    return jsonify(message=message, release=release)

if __name__ == "__main__":
    port = os.getenv('PORT', 8080)
    app.run(host='0.0.0.0', port=port)
