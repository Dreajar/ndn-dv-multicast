from minindn_to_nodes import *

# From GeeksForGeeks article on Bellman-Ford
def bellmanFord(V, edges, src):
    
    dist = [100000000] * V
    dist[src] = 0

    for i in range(V):
        for edge in edges:
            u, v = edge
            if dist[u] != 100000000 and dist[u] + 1 < dist[v]:
                
                # Update shortest distance to node v
                dist[v] = dist[u] + 1
    return dist

def converge(group_members, config_file):
    edges = minindn_to_nodes(config_file)
    all_edges = []
    for e in edges:
        for edge in edges[e]:
            all_edges.append([e, edge])
    nodes = edges.keys()

    V = len(nodes)

    all_routes = {}

    routes = {}

    for n in nodes:
        all_routes[n] = bellmanFord(V, all_edges, n)


    for n in nodes:
        routes[n] = {}
        for i in range(len(all_routes)):
            if i in group_members and i != n:
                routes[n][i] = {}
                for e in edges[n]:
                    routes[n][i][e] = all_routes[e][i]

    return nodes, routes