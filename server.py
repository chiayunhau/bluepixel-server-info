from flask import Flask, jsonify
from fetch_cpu_usage import start_fetching
from gevent.pywsgi import WSGIServer

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
    response = requests.get('https://api.ipify.org')
    if response.status_code == 200:
        print('Your public IP address is:', response.text)
    else:
        print('Failed to retrieve public IP address')
    return jsonify({'cpu_usage': start_fetching(), 'cpu_limit': '200%'})

if __name__ == '__main__':
    # Run the Flask app using the WSGI server
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
