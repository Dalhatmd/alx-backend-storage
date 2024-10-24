#!/usr/bin/env python3
""" inserts to a mongodb collection """


def insert_school(mongo_collection, **kwargs):
    """ function doc """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
