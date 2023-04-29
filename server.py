from flask import Flask, jsonify
from fetch_cpu_usage import start_fetching

app = Flask(__name__)

# Disable CORS in Flask
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/server/cpu')
def server_cpu():
    return jsonify({'cpu_usage': start_fetching(), 'cpu_limit': '200%'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')