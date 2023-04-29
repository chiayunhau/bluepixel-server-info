import requests
import schedule
import time

# Replace with your own Pterodactyl API credentials and server ID
API_URL = 'https://ctrl.cxmpute.com/api/client'
API_KEY = 'ptlc_tTx1NlJbCmfVRXvzJu6O0t76E9j7kGnXZOrWruZRMmA'
SERVER_ID = 'b3683f94-64d0-42ce-94ed-735fe30a8540'

cpu_usage = 0  # Initialize the CPU usage to 0

# Function to fetch the CPU usage data from the Pterodactyl API
def fetch_cpu_usage():
    global cpu_usage
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{API_URL}/servers/{SERVER_ID}/resources', headers=headers)
    if response.status_code == 200:
        cpu_usage = response.json()['attributes']['resources']['cpu_absolute']
    else:
        print('Failed to retrieve server information')

# Schedule the fetch_cpu_usage function to run every 5 seconds
schedule.every(1).seconds.do(fetch_cpu_usage)

# Function to start the scheduled task and return the CPU usage
def start_fetching():
    while True:
        schedule.run_pending()
        time.sleep(1)
        return cpu_usage