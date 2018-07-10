from __future__ import print_function
import requests, time, json

url = 'http://localhost:5000/sanushost/api/v1.0/add_node'
payload = {'NodeID': 'first', 'Neighbors': '[]', 'Type': 'san'}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
print(result)