import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Replace with your own Pterodactyl API credentials and server ID
API_URL = 'https://ctrl.cxmpute.com/api/client'
API_KEY = 'ptlc_tTx1NlJbCmfVRXvzJu6O0t76E9j7kGnXZOrWruZRMmA'
SERVER_ID = 'b3683f94-64d0-42ce-94ed-735fe30a8540'

@app.route('/server/cpu')
def server_cpu():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }

    # Make a GET request to the Pterodactyl API to retrieve server information
    response = requests.get(f'{API_URL}/servers/{SERVER_ID}/resources', headers=headers)

    if response.status_code == 200:
        # Extract the CPU usage value from the response
        cpu_usage = response.json()['attributes']['resources']['cpu_absolute']
        return jsonify({'cpu_usage': cpu_usage})
    else:
        return jsonify({'error': 'Failed to retrieve server information'})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')