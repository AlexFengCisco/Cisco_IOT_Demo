import requests

url = "https://127.0.0.1:5000"

payload  = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data = payload, verify = 'server.crt')
#response = requests.request("GET", url, headers=headers, data = payload)
print(response.text.encode('utf8'))