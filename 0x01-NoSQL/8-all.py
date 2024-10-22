#!/usr/bin/env python3
""" lists documents in a mongodb database """


def list_all(mongo_collection):
    """ lists all documents in mongo_collection """
    if mongo_collection is None:
        return []

    documents = list(mongo_collection.find())
    return documents
