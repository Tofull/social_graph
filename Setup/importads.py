import pandas as pd
import glob
import os
import sys
#from neo4j.v1 import GraphDatabase,  basic_auth
from py2neo import Graph, authenticate
'''
Cypher refcard : https://neo4j.com/docs/cypher-refcard/current/
Launch server : /home/nil/Utils/neo4j-community-3.1.1/bin/neo4j console
Web interface : http://localhost:7474/browser/
Awesome links : https://github.com/neueda/awesome-neo4j
py2neo docs : http://py2neo.org/2.0/
'''


PATH = r'../data/'
VERBOSE = True


def load_ads_data(social_path):
    f = os.path.join(social_path, "annonces.csv")
    df_ads = pd.read_csv(f, index_col=None, header=0)
    f = os.path.join(social_path, "classified_data.csv")
    df_class = pd.read_csv(f, index_col=None, header=0)
    # redefine column names
    df_class.columns = ['title', 'class']
    return df_ads, df_class


def build_query_title(df, verbose=VERBOSE):
    names = pd.unique(df['titre'].values.ravel())
    #if verbose:
    #    print("Unique titles : %d" % len(names))
    queries = [create_title(name.replace("'", "")) for name in names]
    return queries


def create_title(name):
    return "create (`"+name+"`:Ads {name:'"+name+"'})"


def build_query_class(df, verbose=VERBOSE):
    names = pd.unique(df['class'].values.ravel())
    #if verbose:
    #    print("Unique classes : %d" % len(names))
    queries = [create_class(name.replace("'", "")) for name in names]
    return queries


def create_class(name):
    return "create (`"+name+"`:Class {name:'"+name+"'})"


def create_relation_between_user_ads(ads, person, typ):
    return "match (a:Ads),(p:Person) " \
           "where a.name='" + ads + "' and p.name='" + person + "' " \
           "create (p)-[:PUBLISH { type: '" + typ + "'}] ->(a)\n"

def create_relation_between_class_ads(ads, classe):
    return "match (a:Ads),(c:Class) " \
           "where a.name='" + ads + "' and c.name='" + classe + "' " \
           "create (a)-[:BELONGS] ->(c)\n"

def build_query_relationship(df, verbose=VERBOSE):
    #for index, row in df.iterrows():
    #    print(row[6])
    # remove nan lines
    df= df.dropna() 
    queries = [create_relation_between_user_ads(row[6].replace("'", ""), row[2], row[3].replace("'", "")) for index, row in df.iterrows()]
    return queries

def build_query_classification(df, verbose=VERBOSE):
    #for index, row in df.iterrows():
    #    print(row[6])
    # remove nan lines
    df= df.dropna() 
    queries = [create_relation_between_class_ads(row[0].replace("'", ""), row[1].replace("'", "")) for index, row in df.iterrows()]
    return queries



def connect_to_db():
    authenticate("localhost:7474", "neo4j", "social")
    graph = Graph()
    return graph



if __name__ == "__main__":
    datapath = sys.argv[1:][0]
    print(datapath)
    if len(datapath) == 0:    # TODO check
        datapath = PATH
    df_ads, df_class = load_ads_data(datapath)
    queries_class= build_query_class(df_class)
    queries_title= build_query_title(df_ads)
    queries_usertitle= build_query_relationship(df_ads)
    print(queries_title)
    graph = connect_to_db()

    for query in queries_class:
        graph.run(query)
    for query in queries_title:
        graph.run(query)
            
    for query in queries_usertitle:
        graph.run(query)
    
    queries_classification= build_query_classification(df_class)
    for query in queries_class:
        graph.run(query)
    for query in queries_classification:
        graph.run(query)



    print("The end.")


'''
# TESTS
: MATCH (person1)-[:KNOWS]->(person2)
WHERE person1.name= "dimitri"
RETURN person1.name AS Host
collect(person2) AS Dependencies
'''