from flask import Flask, jsonify
from fetch_usage import fetch_cpu_usage, fetch_ram_usage, fetch_disk_usage, fetch_network_usage
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# Disable CORS in Flask
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/cpu-usage')
def get_cpu_usage():
    cpu_usage = fetch_cpu_usage()
    if cpu_usage is None:
        return jsonify({'error': 'Failed to retrieve server information'})
    return jsonify({'cpu_usage': cpu_usage})

@app.route('/ram-usage')
def get_ram_usage():
    ram_usage = fetch_ram_usage()
    if ram_usage is None:
        return jsonify({'error': 'Failed to retrieve server information'})
    return jsonify({'ram_usage': ram_usage})

@app.route('/disk-usage')
def get_disk_usage():
    disk_usage = fetch_disk_usage()
    if disk_usage is None:
        return jsonify({'error': 'Failed to retrieve server information'})
    return jsonify({'disk_usage': disk_usage})

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()