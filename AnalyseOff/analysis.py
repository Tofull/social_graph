import pandas as pd
import glob
import os
import sys
#from neo4j.v1 import GraphDatabase,  basic_auth
from py2neo import Graph, authenticate


def connect_to_db():
    authenticate("localhost:7474", "neo4j", "social")
    g = Graph()
    return g

def basic_statistics():
    # no of relationship / network
    query= ""
    # no of persons per network

    # persons in 1, 2 or 3 networks

    # histogram of relationships per persons


if __name__ == "__main__":
    graph = connect_to_db()

    print("The end.")