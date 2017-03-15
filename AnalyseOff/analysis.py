from py2neo import Graph, authenticate
import pandas as pa
import matplotlib as plt


VERBOSE = True
SAVE = False

def connect_to_db():
    authenticate("localhost:7474", "neo4j", "social")
    graph = Graph()
    return graph


def get_histogram_of_relation():
    query = "MATCH (n) RETURN n.name AS name, SIZE((n)-[:FACEBOOK]->()) AS FACEBOOK,SIZE((n)-[:GOOGLE]->()) AS GOOGLE,SIZE((n)-[:LINKEDIN]->()) AS LINKEDIN"
    cursor = graph.run(query)
    # http://py2neo.org/v3/database.html#py2neo.database.Cursor
    # chose between DataFrame(graph.run("MATCH (a:Person) RETURN a.name, a.born LIMIT 4").data()) (dataframe (dict)) or navigator)
    # and for record in cursor or while cursor.next()

    df= pa.DataFrame(cursor)
    # add columns with sum of relations per individual
    df['TOTAL']= df['FACEBOOK']+df['GOOGLE']+df['LINKEDIN']


    # build histogram
    plt.figure()


    cursor.close()


if __name__ == "__main__":
    graph = connect_to_db()

    get_histogram_of_relation()

    print("\n---------\nThe end.")