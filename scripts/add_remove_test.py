from __future__ import print_function
import requests, time, json

url = 'http://localhost:5000/sanushost/api/v1.0/add_node'
payload = {'NodeID': 'test_sanitizer', 'Neighbors': '["test_entry"]', 'Type': 'san'}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
payload = {'NodeID': 'test_entry', 'Neighbors': '["test_sanitizer"]', 'Type': 'ent'}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
print(result)