import requests
import json

# set the data to send as a dictionary
data = {"croqueta": "pernil"}

# serialize the data to JSON
json_data = json.dumps(data)

# set the headers to specify that the data is JSON
headers = {'Content-type': 'application/json'}

# send the POST request with the serialized JSON data and headers
r = requests.post("https://yoururl/php/prova.php", verify=False, data=json_data, headers=headers)

# print the response from the server
print(r.text)
