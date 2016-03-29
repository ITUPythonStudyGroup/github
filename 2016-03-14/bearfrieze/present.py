import json
import networkx as nx
import matplotlib.pyplot as plt

N = 10

with open('frequencies.json', 'r') as f:
    frequencies = json.loads(f.read())
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    print(frequencies[:10])
    g = nx.Graph()
    for name, weight in frequencies[1:10]:
        g.add_edge(frequencies[0][0], name, weight=weight)
    pos = nx.spring_layout(g)
    nx.draw_networkx_edges(g, pos, width=1)
    nx.draw_networkx_nodes(g, pos, node_size=500)
    nx.draw_networkx_labels(g, pos, font_size=12, font_family='sans-serif')
    plt.show()
