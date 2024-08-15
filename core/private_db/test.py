from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

try:
    database = client["mydatabase"]
    collection = database["customers"]
    result = collection.find_one({"name": "John", "address": "Highway 37"})
    print(result)
    print("Connected successfully!")
    client.close()
except Exception as e:
    print("Connection error: ", e)
    client.close()