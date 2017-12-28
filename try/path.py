import os
import pickle

from db import query
from config import PROJECT_DIR

import networkx as nx

pkl = os.path.join(PROJECT_DIR, 'path.pkl')

def create_graph(edge_table, node_table):
	edge_set = query("SELECT * FROM " + edge_table)
	node_set = query("SELECT * FROM " + node_table)

	graph = nx.DiGraph()
	for item in edge_set:
		graph.add_edges_from([(item["source"], item["target"], {"length":item["length"], "id":item["id"]})])
	for item in node_set:
		if item["node"] in graph:
			graph.node[item["node"]]["x"] = item["x"]
			graph.node[item["node"]]["y"] = item["y"]
	return graph

def graphs():

	taxi_graph_1 = create_graph("edge1", "node")
	taxi_graph_2 = create_graph("edge2", "node")
	drive_graph = create_graph("c_edge", "c_node")

	return taxi_graph_1, taxi_graph_2, drive_graph

taxi_graph_1, taxi_graph_2, drive_graph = graphs()

def generate_path():
	path = {}
	# taxi_graph_1.add_edges_from(taxi_graph_2.edges)

	air_land = query('select landing_point from aircraft group by landing_point')
	air_park = query('select parking_point from aircraft group by parking_point')
	air_departure1 = query('select departure_point1 from aircraft group by departure_point1')
	air_departure2 = query('select departure_point2 from aircraft group by departure_point2')
	car_unload = query('select unload_dock from position GROUP BY unload_dock')
	car_service = query('select service_source from position GROUP BY service_source')

	for park in air_park:
		park = park['parking_point']
		for land in air_land:
			land = land['landing_point']
			path[(land, park)] = nx.shortest_path(taxi_graph_1, land, park, weight='length')
		for departure1 in air_departure1:
			departure1 = departure1['departure_point1']
			path[(park, departure1)] = nx.shortest_path(taxi_graph_1, park, departure1, weight='length')
		for departure2 in air_departure2:
			departure2 = departure2['departure_point2']
			path[(park, departure2)] = nx.shortest_path(taxi_graph_1, park, departure2, weight='length')
		for service in car_service:
			service = service['service_source']
			path[(service, park)] = nx.shortest_path(drive_graph, service, park, weight='length')
		for unload in car_unload:
			unload = unload['unload_dock']
			path[(park, unload)] = nx.shortest_path(drive_graph, park, unload, weight='length')

	return path


if os.path.exists(pkl):
	with open(pkl, 'rb') as file:
		path = pickle.load(file)
else:
	path = generate_path()
	with open(pkl, 'wb') as file:
		pickle.dump(path, file)
