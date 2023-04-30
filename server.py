from flask import Flask, jsonify
from fetch_usage import fetch_cpu_usage, fetch_ram_usage, fetch_disk_usage, fetch_state
from gevent.pywsgi import WSGIServer
import requests

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

@app.route('/state')
def get_state():
    current_state = fetch_state()
    if current_state is None:
        return jsonify({'error': 'Failed to retrieve server information'})
    return jsonify({'current_state': current_state})

@app.route('/start-server')
def start_server():
    endpoint = f'https://ctrl.cxmpute.com/api/client/servers/b3683f94-64d0-42ce-94ed-735fe30a8540/power'
    headers = {'Authorization': f'Bearer ptlc_tTx1NlJbCmfVRXvzJu6O0t76E9j7kGnXZOrWruZRMmA'}
    data = {'signal': 'start'}
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 204:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()