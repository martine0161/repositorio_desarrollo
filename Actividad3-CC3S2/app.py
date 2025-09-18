import os
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    return {
        'message': os.getenv('MESSAGE', 'Hello DevOps!'),
        'port': os.getenv('PORT', '8080'),
        'release': os.getenv('RELEASE', 'v1.0.0'),
        'timestamp': time.time()
    }

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': time.time()}

@app.route('/ready')
def ready():
    return {'status': 'ready', 'timestamp': time.time()}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='127.0.0.1', port=port, debug=True)