#!/usr/bin/env python3
""" update """


def update_topics(mongo_collection, name, topics):
    """ updates a topic based on the name """
    to_update = {"name": name}
    update = {"$set": {"topics": topics}}
    result = mongo_collection.update_many(to_update, update)
