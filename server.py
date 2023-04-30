from flask import Flask, jsonify
from fetch_usage import fetch_cpu_usage, fetch_ram_usage, fetch_disk_usage, fetch_state
from gevent.pywsgi import WSGIServer
import requests
from flask import Flask, request, jsonify
from backendtestings import login, add_cash, deduct_cash, transfer_cash, get_balance, get_admin_status

app = Flask(__name__)

# Disable CORS in Flask
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

# Define the endpoint for getting the user's balance
@app.route('/api/balance/<username>')
def balance_endpoint(username):
    balance = get_balance(username)
    return jsonify(balance)

# Define the endpoint for getting the user's admin status
@app.route('/api/admin/<username>')
def admin_endpoint(username):
    admin = get_admin_status(username)
    return jsonify(admin)

# Endpoint for password-only login
@app.route('/login', methods=['POST'])
def login_endpoint():
    password = request.json.get('password')
    result = login(password)
    return jsonify(result)

# Endpoint for adding cash to a user's account
@app.route('/add_cash', methods=['POST'])
def add_cash_endpoint():
    password = request.json.get('password')
    amount = request.json.get('amount')
    result = add_cash(password, amount)
    return jsonify(result)

# Endpoint for deducting cash from a user's account
@app.route('/deduct_cash', methods=['POST'])
def deduct_cash_endpoint():
    password = request.json.get('password')
    amount = request.json.get('amount')
    result = deduct_cash(password, amount)
    return jsonify(result)

# Endpoint for transferring cash from one user to another
@app.route('/transfer_cash', methods=['POST'])
def transfer_cash_endpoint():
    from_password = request.json.get('from_password')
    to_username = request.json.get('to_username')
    amount = request.json.get('amount')
    result = transfer_cash(from_password, to_username, amount)
    return jsonify(result)

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