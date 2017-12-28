import networkx as nx
from matplotlib import pyplot as plt

G = nx.Graph()
G.add_node(1,pos=(1,2))
G.add_node(2,pos=(3,4))
pos = nx.get_node_attributes(G,'pos')
print(pos)
# nx.draw(G,pos)
# plt.show()
