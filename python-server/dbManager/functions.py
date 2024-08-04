from pymongo import MongoClient
import hashlib
import json

def _make_immutable(obj):
    if isinstance(obj, dict):
        return frozenset((k, _make_immutable(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return tuple(_make_immutable(i) for i in obj)
    elif isinstance(obj, set):
        return frozenset(_make_immutable(i) for i in obj)
    else:
        return obj


def connect_db(uri):
    try:
        client = MongoClient(uri)
        print("Connected to the database")
        return client
    except Exception as e:
        raise Exception("Unable to connect to the database due to the following error: ", e)


def create_or_open_database(client, database_name):
    try:
        database = client.get_database(database_name)
        print("Connected to the database")
        return database
    except Exception as e:
        raise Exception("Unable to connect to the database due to the following error: ", e)


def create_or_open_collection(database, collection_name):
    try:
        collection = database.get_collection(collection_name)
        print("Connected to the collection")
        return collection
    except Exception as e:
        raise Exception("Unable to connect to the collection due to the following error: ", e)


def insert_one_data(collection, data):
    if collection.find_one(data):
        print("Data already exists")
    else:
        collection.insert_one(data)
        print("Data inserted successfully")


def insert_many_datas(collection, data_list):
    query_conditions = {"$or": data_list}

    existing_records = list(collection.find(query_conditions, {"_id": 0}))
    existing_data_set = {_make_immutable(record) for record in existing_records}

    to_insert = [data for data in data_list if _make_immutable(data) not in existing_data_set]

    if to_insert:
        # 批量插入不存在的数据
        collection.insert_many(to_insert)
        print(f"Insert {len(to_insert)} datas successfully")
    else:
        print("All datas already exist")


def delete_one_data(collection, data):
    if collection.find_one(data):
        collection.delete_one(data)
        print("Data deleted successfully")
    else:
        print("Data not found")

def clear_collection(collection):
    collection.delete_many({})
    print("Collection cleared")