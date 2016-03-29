import json
import networkx as nx
import matplotlib.pyplot as plt

N = 10
WIDTH = 5

with open('frequencies.json', 'r') as f:
    frequencies = json.loads(f.read())
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    master = frequencies[0]
    frequencies = frequencies[1:N]
    g = nx.Graph()
    max_weight = max(f[1] for f in frequencies)
    for name, weight in frequencies:
        g.add_edge(master[0], name, weight=(weight/max_weight) * WIDTH)
    edgewidth = [ d['weight'] for (u,v,d) in g.edges(data=True)]
    pos = nx.spring_layout(g, iterations=50)
    nx.draw_networkx_edges(g, pos, width=edgewidth)
    nx.draw_networkx_nodes(g, pos, node_size=500)
    nx.draw_networkx_labels(g, pos, font_size=12, font_family='sans-serif')
    plt.show()
