import model
import networkx as nx
import logging
import pymysql.cursors

import model

class NetworkxUtil(object):

    def __init__(self, db_config: model.DbConfig, db: str) -> None:
        self.db_config = db_config
        self.db = db
        self.graph = model.Graph()
        self.graph.load_from_db(db_config, db)
        self.n_graph = self.build_graph()
        self.nondirected_graph = self.build_nondirected_graph()

    def build_graph(self) -> nx.DiGraph:
        n_graph = nx.DiGraph() 

        # Add nodes
        for node in self.graph.nodes:
            n_graph.add_node(node.name)

        # Add edges
        for edge in self.graph.edges:
            n_graph.add_edge(edge.source, edge.target)

        return n_graph

    def build_nondirected_graph(self) -> nx.DiGraph:
        nondirected_graph = nx.Graph()

        for node in self.graph.nodes:
            nondirected_graph.add_node(node.name)

        for edge in self.graph.edges:
            nondirected_graph.add_edge(edge.source, edge.target)
        return nondirected_graph        

    def get_all_path(self, source, target, cutoff: int=-1, only_directed: bool=False):
        if only_directed:
            if cutoff > 0:
                return list(nx.all_simple_paths(self.n_graph, source, target, cutoff=cutoff))
            else:
                return list(nx.all_simple_paths(self.n_graph, source, target))
        else:
            if cutoff > 0:
                return list(nx.all_simple_paths(self.nondirected_graph, source, target, cutoff=cutoff))
            else:
                return list(nx.all_simple_paths(self.nondirected_graph, source, target))


    @staticmethod
    def page_rank(n_graph: nx.DiGraph) -> map:
        # Compute rank
        page_rank_map = nx.pagerank(n_graph)
        logging.info("Compute page rank: " + str(page_rank_map))
        return page_rank_map

    @staticmethod
    def update_db_weight(db_config: model.DbConfig, db: str, page_rank_map: map) -> None:

        connection = pymysql.connect(host=db_config.host,
                                    user=db_config.user,
                                    password=db_config.password,
                                    database=db_config.db,
                                    cursorclass=pymysql.cursors.DictCursor)
                                            
        with connection.cursor() as cursor:

            for name, rank_value in page_rank_map.items():
                sql = "UPDATE {}.nodes SET weight = {} WHERE name = '{}';".format(db, rank_value, name)
                logging.info("Execute the SQL: " + sql)
                cursor.execute(sql)
        
        connection.commit()

    def update_wight(self) -> None:
        page_rank_map = NetworkxUtil.page_rank(self.n_graph)
        NetworkxUtil.update_db_weight(self.db_config, self.db, page_rank_map)

def main() -> None:
    db_config = model.DbConfig("localhost", "root", "wawa316", "")
    db = "cyberpunk_edgerunner"
    util = NetworkxUtil(db_config, db)
    #util.update_wight()

    paths = util.get_all_path("david", "rebecca", only_directed=True)
    print(list(paths))
    #for path in paths:
    #    print(path)



if __name__ == "__main__":
    main()