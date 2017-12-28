import networkx as nx
import pymysql.cursors
from db import query
from networkx.readwrite import json_graph
import flask
import json



def create_graph( edge_table, node_table):
    edge_set = query( "SELECT * FROM " + edge_table)
    node_set = query( "SELECT * FROM " + node_table)
    graph = nx.DiGraph()
    for item in edge_set:
        graph.add_edges_from([(item["source"], item["target"], {"length":item["length"], "id":item["id"]})])
        for item in node_set:
                if item["node"] in graph:
                        graph.node[item["node"]]["x"] = item["x"]
                        graph.node[item["node"]]["y"] = item["y"]
    return graph


if __name__ == '__main__':
    # taxi_graph_1 = create_graph("edge1", "node")
    taxi_graph_1 = create_graph("edge1", "node")

    d = json_graph.node_link_data(taxi_graph_1)  # node-link format to serialize
    # write json
    json.dump(d, open('force/force.json', 'w'),indent=4)
    # Serve the file over http to allow for cross origin requests
    app = flask.Flask(__name__, static_folder="force")

    @app.route('/<path:path>')
    def static_proxy(path):
        return app.send_static_file(path)

    print('\nGo to http://localhost:8000/force.html to see the example\n')
    app.run(port=8000)
