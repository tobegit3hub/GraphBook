import pymysql.cursors
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class Node:
    id: int
    name: str
    display_name: str = ""
    note: str = ""
    weight: float = 0.0
    #image: str = ""

@dataclass
class Edge:
    id: int
    source: int
    target: str
    relation: str = ""

@dataclass
class Group:
    id: int
    name: str
    node_name: str

class Graph:
    def __init__(self) -> None:
        self.nodes = []
        self.edges = []
        self.groups = []

    def __str__(self) -> str:
        return "Nodes: {},\nEdges: {},\nGroups: {}".format(self.nodes, self.edges, self.groups)

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def add_group(self, group: Group) -> None:
        self.groups.append(group)
    
    def load_from_db(self, connection) -> None:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM nodes"
            cursor.execute(sql)
            result_set = cursor.fetchall()
            for item in result_set:
                node = Node(item["id"], item["name"], item["display_name"], item["note"], item["weight"])
                self.add_node(node)
                logging.info("Load node: {}".format(node))

            sql = "SELECT * FROM edges"
            cursor.execute(sql)
            result_set = cursor.fetchall()
            for item in result_set:
                edge = Edge(item["id"], item["source"], item["target"], item["relation"])
                self.add_edge(edge)
                logging.info("Load edge: {}".format(edge))

            sql = "SELECT * FROM teams"
            cursor.execute(sql)
            result_set = cursor.fetchall()
            for item in result_set:
                group = Group(item["id"], item["name"], item["node_name"])
                self.add_group(group)
                logging.info("Load group: {}".format(group))


def main():
    mysql_host = "localhost"
    mysql_user = "root"
    mysql_password = "root"
    mysql_db = "cyberpunk_edgerunner"

    # Connect to the database
    connection = pymysql.connect(host=mysql_host,
                                user=mysql_user,
                                password=mysql_password,
                                database=mysql_db,
                                cursorclass=pymysql.cursors.DictCursor)


    graph = Graph()
    graph.load_from_db(connection)
    print(graph)

if __name__ == "__main__":
    main()


