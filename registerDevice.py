import urllib.request
import json
import requests
import socket

ipRequest = urllib.request.Request('https://api.ipify.org?format=json')
ipResponse = urllib.request.urlopen(ipRequest).read()
data = json.loads(ipResponse)
print(data['ip'])

hostname = socket.gethostname()

print(hostname)

payload = {'name': hostname, 'address': data['ip']}
r = requests.get('http://198.211.109.9:8000/SafeHomeDatabase/createDevice/?', params=payload)
print(r)