#!/usr/bin/env python3
""" gets logs from a mongodb database"""
from pymongo import MongoClient


def get_logs():
    """ gets and formats logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db['nginx']

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    document_count = collection.count_documents({})

    print(f"{document_count} logs")
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    to_find = {"method": "GET", "path": "/status"}
    status_check = collection.count_documents(to_find)
    print(f"{status_check} status check")


get_logs()
