#!/usr/bin/env python3
""" gets schools by topic """


def schools_by_topic(mongo_collection, topic):
    """ function doc """
    to_find = {"topics": topic}
    schools = mongo_collection.find(to_find)
    return schools
