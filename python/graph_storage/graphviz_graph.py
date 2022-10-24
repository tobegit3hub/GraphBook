import model
import graphviz

def build_graph(graph: model.Graph) -> None:
    g_graph = graphviz.Digraph()

    # Add nodes
    for node in graph.nodes:
        g_graph.node(node.name, node.display_name)

    # Add edges
    for edge in graph.edges:
        g_graph.edge(edge.source, edge.target, edge.relation)

    g_graph.view()

def main():
    db_config = model.DbConfig("localhost", "root", "root", "cyberpunk_edgerunner")
    graph = model.Graph()
    graph.load_from_db(db_config)
    build_graph(graph)

if __name__ == "__main__":
    main()