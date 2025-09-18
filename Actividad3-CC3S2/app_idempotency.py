import os
from flask import Flask, jsonify
import time

app = Flask(__name__)
counter = 0

@app.route('/idempotent')
def idempotent():
    return {'message': 'Always same', 'timestamp': 'fixed'}

@app.route('/non-idempotent')  
def non_idempotent():
    global counter
    counter += 1
    return {'message': f'Counter: {counter}', 'timestamp': time.time()}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)