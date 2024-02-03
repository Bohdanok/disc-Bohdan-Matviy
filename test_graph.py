
import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, groupby
from networkx.algorithms import tree
from networkx.algorithms import bellman_ford_predecessor_and_distance


# You can use this function to generate a random graph with 'num_of_nodes' vertexes
# and 'completeness' probability of an edge between any two vertexes
# If 'directed' is True, the graph will be directed
# If 'draw' is True, the graph will be drawn
def gnp_random_connected_graph(num_of_nodes: int,
                               completeness: int,
                               directed: bool = False,
                               draw: bool = False):
    """
    Generates a random graph, similarly to an Erdős-Rényi 
    graph, but enforcing that the resulting graph is conneted (in case of undirected graphs)
    """


    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edges = combinations(range(num_of_nodes), 2)
    G.add_nodes_from(range(num_of_nodes))

    for _, node_edges in groupby(edges, key = lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        if random.random() < 0.5:
            random_edge = random_edge[::-1]
        G.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < completeness:
                G.add_edge(*e)
                
    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.randint(-5, 20)
                
    if draw: 
        plt.figure(figsize=(10,6))
        if directed:
            # draw with edge weights
            pos = nx.arf_layout(G)
            nx.draw(G,pos, node_color='lightblue', 
                    with_labels=True,
                    node_size=500, 
                    arrowsize=20, 
                    arrows=True)
            labels = nx.get_edge_attributes(G,'weight')
            nx.draw_networkx_edge_labels(G, pos,edge_labels=labels)
            
        else:
            nx.draw(G, node_color='lightblue', 
                with_labels=True, 
                node_size=500)
    # print([G])
    return G

G = gnp_random_connected_graph(4, 1, True, True)
# G._adj = {0: {3: {'weight': -1}, 1: {'weight': 12}, 2: {'weight': -4}}, 1: {0: {'weight': 12}, 2: {'weight': 14}, 3: {'weight': -4}}, 2: {0: {'weight': -4}, 1: {'weight': 14}, 3: {'weight': 5}}, 3: {0: {'weight': -1}, 1: {'weight': -4}, 2: {'weight': 5}}}
# def check_for_simple_cycles(graph:nx.classes.graph.Graph)->bool:
#     '''
#     Check for simple path.
#     Returns True if the graph has one
#     graph:nx.classes.graph.Graph
#     '''
#     visited = set()
#     # print( graph._adj.items())
#     simple_graph = {key:list(j for j in value.keys()) for key, value in graph._adj.items()}
#     # print(simple_graph)
#     def check_node(vertex):
#         visited.add(vertex)
#         for adj_node in simple_graph.get(vertex, ()):
#             if adj_node in visited or check_node(adj_node):
#                 return True
#         visited.remove(vertex)
#         return False
#     return any(check_node(i) for i in simple_graph)


def prim(graph: nx.classes.graph.Graph) -> nx.classes.graph.Graph:
    '''
    Prim's algorithm
    Uses and returns an object of class nx.classes.graph.Graph
    '''

    length = len(graph.nodes.keys()) - 1
    output_graph = nx.Graph()
    vertexes = [0]

    while len(output_graph.edges) < length:
        min_edge = (0, 0, float('inf'))

        for vertex in vertexes:
            for neighbor, weight_dict in graph._adj[vertex].items():
                weight = weight_dict['weight']
                min_edge = min(min_edge, (vertex, neighbor, weight), key=lambda x: x[2])

        if min_edge[1] not in vertexes:
            vertexes.append(min_edge[1])
            output_graph.add_edge(min_edge[0], min_edge[1], weight=min_edge[2])
        graph.remove_edge(min_edge[0], min_edge[1])
    return output_graph

#************************************************************
# G2 = G
# print(prim(G2).edges)
# print('**********************************')
# mstp = tree.minimum_spanning_tree(G, algorithm="prim")
# print(mstp.edges)
# # print(f'{G.edges = }')

# graph = nx.classes.graph.Graph()


def bellman_ford(graph:nx.classes.graph.Graph, sourse:int)->dict | str:
    '''
    Bellman-Ford algorithm which allows to know all the passes from the sourse
    returns dictinary {node: distanse:int}

    If negative cycle is detected returns a message:
    'Negative cycle detected!'

    '''
    lenght = len(graph.edges)
    shortest_path = {i:float('inf') for i in range(len(graph.nodes))}
    shortest_path[sourse] = 0

    ###Calculate distances

    for _ in range(lenght):
        for sour, dest, weight in list(G.edges(data=True)):
            if shortest_path[dest] > shortest_path[sour] + weight['weight']:
                shortest_path[dest] = weight['weight'] + shortest_path[sour]

    ###Check for a negative cycle

    for sour, dest, weight in list(G.edges(data=True)):
        if shortest_path[dest] > shortest_path[sour] + weight['weight']:
            return 'Negative cycle detected!'
    return shortest_path

# # print(list(G.edges(data=True)))
# try:
#     print(bellman_ford_predecessor_and_distance(G, 0)[1])
#     # pred, dist = bellman_ford_predecessor_and_distance(G, 0)
#     # for k, v in dist.items():
#     #     print(f"Distance to {k}:", v)
# except:
#     print("Negative cycle detected")
# print('***********************************')
# print(bellman_ford(G, 0))

