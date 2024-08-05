import datetime

import functions

uri = "mongodb+srv://lin:1024@xlincluster.cqjabof.mongodb.net/?retryWrites=true&w=majority&appName=xLinCluster"
client = functions.connect_db(uri)
if client is None:
    print("Client is None")
    exit(1)

database = functions.create_or_open_database(client, "test1")
if database is None:
    print("Database is None")
    exit(1)

collection = functions.create_or_open_collection(database, "collection1")
if collection is None:
    print("Collection is None")
    exit(1)

peopleDocuments = [
    {
        "name": { "first": "Alan", "last": "Turing" },
        "birth": datetime.datetime(1912, 6, 23),
        "death": datetime.datetime(1954, 6, 7),
        "contribs": [ "Turing machine", "Turing test", "Turingery" ],
        "views": 1250000
    },
    {
        "name": { "first": "Grace", "last": "Hopper" },
        "birth": datetime.datetime(1906, 12, 9),
        "death": datetime.datetime(1992, 1, 1),
        "contribs": [ "Mark I", "UNIVAC", "COBOL" ],
        "views": 3860000
    },
    {
        "name": { "first": "Chandler", "last": "Bing" },
        "birth": datetime.datetime(1907, 3, 9),
        "death": datetime.datetime(1999, 2, 2),
        "contribs": [ "Friends"],
        "views": 3860000
    }
]

functions.insert_many_datas(collection, peopleDocuments)
# functions.clear_collection(collection)
result = collection.find_one({ "name.last": "Bing" })
# print results
print("Document found:\n", result)

client.close()