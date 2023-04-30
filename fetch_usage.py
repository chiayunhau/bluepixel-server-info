import requests

API_URL = 'https://ctrl.cxmpute.com/api/client'
API_KEY = 'ptlc_tTx1NlJbCmfVRXvzJu6O0t76E9j7kGnXZOrWruZRMmA'
SERVER_ID = 'b3683f94-64d0-42ce-94ed-735fe30a8540'

# Function to fetch CPU usage data from the Pterodactyl API
def fetch_cpu_usage():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{API_URL}/servers/{SERVER_ID}/resources', headers=headers)
    if response.status_code == 200:
        data = response.json()['attributes']['resources']
        cpu_usage = data['cpu_absolute']
        return cpu_usage
    else:
        print('Failed to retrieve server information')
        return None

# Function to fetch RAM usage data from the Pterodactyl API
def fetch_ram_usage():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{API_URL}/servers/{SERVER_ID}/resources', headers=headers)
    if response.status_code == 200:
        data = response.json()['attributes']['resources']
        ram_usage = data['memory_bytes']
        ram_gb = round(ram_usage / (1024**3), 2)
        return ram_gb
    else:
        print('Failed to retrieve server information')
        return None

# Function to fetch disk usage data from the Pterodactyl API
def fetch_disk_usage():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{API_URL}/servers/{SERVER_ID}/resources', headers=headers)
    if response.status_code == 200:
        data = response.json()['attributes']['resources']
        disk_usage = data['disk_bytes']
        disk_usage_gb = round(disk_usage / (1024**3), 2)
        return disk_usage_gb
    else:
        print('Failed to retrieve server information')
        return None

# Function to fetch network usage data from the Pterodactyl API
def fetch_network_usage():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{API_URL}/servers/{SERVER_ID}/resources', headers=headers)
    if response.status_code == 200:
        data = response.json()['attributes']['resources']
        network_rx = data['network_rx_bytes']
        network_tx = data['network_tx_bytes']
        return {'network_rx': network_rx, 'network_tx': network_tx}
    else:
        print('Failed to retrieve server information')
        return None
