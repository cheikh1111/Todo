import requests

response = requests.get("http://192.168.1.66:80/api",headers={'username':'cheikh','password':'22391978'})


print(response.status_code)

print(response.json())