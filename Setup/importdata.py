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


def load_social_network_data(social_path):
    files = glob.glob(os.path.join(social_path, "relations*.csv"))
    df_from_each_file = (pd.read_csv(f, index_col=None, header=0) for f in files)
    df = pd.concat(df_from_each_file, ignore_index=True)
    # redefine column names
    df.columns = ['network', 'name1', 'name2', 'relationship']
    return df


def create_network(name):
    return "create (`" + name + "`:Network {name:'" + name + "'})"


def create_names(name):
    return "create (`"+name+"`:Person {name:'"+name+"'})"


def create_relation_to_network(network, person):
    return "match (n:Network),(p:Person) " \
           "where n.name='" + network + "' and p.name='" + person + "' " \
           "create (p)-[:BELONGS] ->(m)\n"


def create_relation_between_persons(network, name1, name2, relation):
    return "match (n:Person),(m:Person) " \
           "where n.name='" + name1 + "' and m.name='" + name2 + "' " \
           "create (n)-[:KNOWS {network: '"+network+"', relation: '" + relation + "'}] ->(m)\n"


def build_query_network(df, verbose=VERBOSE): # useful ?
    network_names = df.network.unique()
    if verbose:
        print("Networks")
        print(network_names)
    queries = [create_network(name) for name in network_names]
    if verbose:
        print("Queries")
        print(queries)
    return queries


def build_query_users(df, verbose=VERBOSE):
    names = pd.unique(df[['name1', 'name2']].values.ravel())
    if verbose:
        print("Unique names : %d" % len(names))
    queries = [create_names(name) for name in names]
    return queries


#def build_query_relation_to_network(df, verbose= VERBOSE):


def build_query_relationship(df, verbose=VERBOSE):
#    for index, row in df.iterrows():
#        print(row[1])
    queries = [create_relation_between_persons(row[0], row[1], row[2], row[3]) for index, row in df.iterrows()]
    return queries


def connect_to_db():
    '''
    driver = GraphDatabase.driver('bolt://localhost', auth=basic_auth("neo4j", "social"))
    session= driver.session()
    return session
    '''
    authenticate("localhost:7474", "neo4j", "social")
    graph = Graph()
    return graph



if __name__ == "__main__":
    datapath = sys.argv[1:][0]
    print(datapath)
    if len(datapath) == 0:    # TODO check
        datapath = PATH
    df_social = load_social_network_data(datapath)
    if VERBOSE:
        print("Social relationships")
        print(df_social.describe())
    list_network_queries = build_query_network(df_social)
    list_users_queries = build_query_users(df_social)
    list_relations = build_query_relationship(df_social)
    #session = connect_to_db()
    #result = session.run
    graph = connect_to_db()
    for query in list_users_queries:
        graph.run(query)
    for query in list_relations:
        graph.run(query)
    print("The end.")


'''
# TESTS
: MATCH (person1)-[:KNOWS]->(person2)
WHERE person1.name= "dimitri"
RETURN person1.name AS Host
collect(person2) AS Dependencies
'''