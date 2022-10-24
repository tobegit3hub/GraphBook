import model
import networkx as nx
import logging
import pymysql.cursors

import model

def build_graph(graph: model.Graph) -> nx.DiGraph:
    n_graph = nx.DiGraph() 

    # Add nodes
    for node in graph.nodes:
        n_graph.add_node(node.name)

    # Add edges
    for edge in graph.edges:
        n_graph.add_edge(edge.source, edge.target)

    return n_graph

def page_rank(n_graph: nx.DiGraph) -> map:
    # Compute rank
    page_rank_map = nx.pagerank(n_graph)
    logging.info("Compute page rank: " + str(page_rank_map))
    return page_rank_map


def update_weight(db_config: model.DbConfig, page_rank_map: map) -> None:

    connection = pymysql.connect(host=db_config.host,
                                user=db_config.user,
                                password=db_config.password,
                                database=db_config.db,
                                cursorclass=pymysql.cursors.DictCursor)
                                        
    with connection.cursor() as cursor:

        for name, rank_value in page_rank_map.items():
            sql = "UPDATE nodes SET weight = {} WHERE name = \"{}\";".format(rank_value, name)
            logging.info("Execute the SQL: " + sql)
            cursor.execute(sql)
    
    connection.commit()


def main() -> None:
    graph = model.Graph()
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph.load_from_db(db_config)
    
    n_graph = build_graph(graph)
    page_rank_map = page_rank(n_graph)
    update_weight(db_config, page_rank_map)


if __name__ == "__main__":
    main()