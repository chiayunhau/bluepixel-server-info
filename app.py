from flask import Flask, jsonify
import os
import requests
import json

app = Flask(__name__)

@app.route('/cpu-usage')
def get_cpu_usage():
    # Set the API key and API URL
    api_key = os.environ.get('PTERODACTYL_API_KEY')
    api_url = 'https://ctrl.cxmpute.com/api/client'


    # Set the headers for the API requests
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Accept': 'application/vnd.pterodactyl.v1+json',
        'Content-Type': 'application/json'
    }

    # Replac   e {server_id} with your actual server ID
    server_id = 'b3683f94-64d0-42ce-94ed-735fe30a8540'

    # Get the server's resource utilization
    response = requests.get(api_url + '/servers/' + server_id + '/resources', headers=headers)

    # Extract the JSON string from the response
    response_json = response.text

    # Parse the JSON string into a Python dictionary
    response_dict = json.loads(response_json)
    
    # Access the value of the "cpu_absolute" key
    cpu_usage = response_dict['attributes']['resources']['cpu_absolute']

    return jsonify({'cpu_usage': cpu_usage})

if __name__ == '__main__':
    # Change the port to match your desired port number
    app.run(host='0.0.0.0', port=8000, debug=True)

