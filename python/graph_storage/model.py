from array import array
import pymysql.cursors
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    db: str

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
    
    def load_from_db(self, db_config: DbConfig) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
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

    def get_nodes_for_frontend(self, db_config: DbConfig, db: str, limit_num: int=-1) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if limit_num > 0:
                sql = "SELECT id as row_id, name, display_name, note, weight FROM {}.nodes ORDER BY id LIMIT %s".format(db)
                cursor.execute(sql, (limit_num))
            else:
                sql = "SELECT id as row_id, name, display_name, note, weight FROM {}.nodes".format(db)
                cursor.execute(sql)
            
            result_set = cursor.fetchall()
            return result_set

    def get_edges_for_frontend(self, db_config: DbConfig, db: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.edges".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            return result_set

    def get_groups_for_frontend(self, db_config: DbConfig, db: str) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            sql = "SELECT * FROM {}.teams".format(db)
            cursor.execute(sql)
            result_set = cursor.fetchall()
            return result_set

    def update_nodes(self, db_config: DbConfig, db: str, insert_nodes: array, update_nodes: array, delete_nodes: array) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if len(insert_nodes) > 0:
                sql = "INSERT INTO {}.nodes (name, display_name, note) VALUES (%s, %s, %s)".format(db);
                insert_nodes_data = [(insert_node["name"], insert_node["display_name"], insert_node["note"]) for insert_node in insert_nodes]
                print("Try to execute sql: {}, data: {}".format(sql, insert_nodes_data))
                cursor.executemany(sql, insert_nodes_data)

            for update_node in update_nodes:
                sql = "UPDATE {}.nodes SET display_name=%s, note=%s WHERE name=%s".format(db)
                update_nodes_data = (update_node["display_name"], update_node["note"], update_node["name"])
                print("Try to execute sql: {}, data: {}".format(sql, update_nodes_data))
                cursor.execute(sql, update_nodes_data)

            if len(delete_nodes) > 0:
                sql = "DELETE FROM {}.nodes WHERE name=%s".format(db);
                delete_nodes_data = [(delete_node["name"]) for delete_node in delete_nodes]
                print("Try to execute sql: {}, data: {}".format(sql, delete_nodes_data))
                cursor.executemany(sql, delete_nodes_data)

        connection.commit()

    def update_edges(self, db_config: DbConfig, db: str, insert_edges: array, update_edges: array, delete_edges: array) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if len(insert_edges) > 0:
                sql = "INSERT INTO {}.edges (source, target, relation, note) VALUES (%s, %s, %s, %s)".format(db);
                insert_edges_data = [(insert_edge["source"], insert_edge["target"], insert_edge["relation"], insert_edge["note"]) for insert_edge in insert_edges]
                print("Try to execute sql: {}, data: {}".format(sql, insert_edges_data))
                cursor.executemany(sql, insert_edges_data)

            for update_edge in update_edges:
                sql = "UPDATE {}.edges SET relation=%s, note=%s WHERE source=%s AND target=%s".format(db)
                update_edges_data = (update_edge["relation"], update_edge["note"], update_edge["source"], update_edge["target"])
                print("Try to execute sql: {}, data: {}".format(sql, update_edges_data))
                cursor.execute(sql, update_edges_data)

            if len(delete_edges) > 0:
                sql = "DELETE FROM {}.edges WHERE source=%s AND target=%s".format(db);
                delete_edges_data = [(delete_edge["source"], delete_edge["target"]) for delete_edge in delete_edges]
                print("Try to execute sql: {}, data: {}".format(sql, delete_edges_data))
                cursor.executemany(sql, delete_edges_data)

        connection.commit()

    def update_groups(self, db_config: DbConfig, db: str, insert_groups: array, update_groups: array, delete_groups: array) -> None:
        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:
            if len(insert_groups) > 0:
                sql = "INSERT INTO {}.teams (group_name, node_name) VALUES (%s, %s)".format(db);
                insert_groups_data = [(insert_group["group_name"], insert_group["node_name"]) for insert_group in insert_groups]
                print("Try to execute sql: {}, data: {}".format(sql, insert_groups_data))
                cursor.executemany(sql, insert_groups_data)

            for update_group in update_groups:
                sql = "UPDATE {}.teams SET group_name=%s, node_name=%s WHERE id=%s".format(db)
                update_groups_data = (update_group["group_name"], update_group["node_name"], update_group["id"])
                print("Try to execute sql: {}, data: {}".format(sql, update_groups_data))
                cursor.execute(sql, update_groups_data)

            if len(delete_groups) > 0:
                sql = "DELETE FROM {}.teams WHERE id=%s".format(db);
                delete_groups_data = [(delete_group["id"]) for delete_group in delete_groups]
                print("Try to execute sql: {}, data: {}".format(sql, delete_groups_data))
                cursor.executemany(sql, delete_groups_data)

        connection.commit()


def main():
    db_config = DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph = Graph()
    graph.load_from_db(db_config)
    print(graph)


if __name__ == "__main__":
    main()


