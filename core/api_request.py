import requests

url = "http://127.0.0.1:8000/request-apm/"
file_path = "test_apm.apm"
with open(file_path,"rb") as file:
    binary_data = file.read()
    response = requests.post(url,data=binary_data,stream=True)

for chunk in response.iter_content(chunk_size=1024):
    print(chunk)