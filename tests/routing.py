from minindn_to_nodes import *
from copy import deepcopy

def bellman_ford(V, edges, group_members):
    # initialize
    dist = {}
    min_dist = {}
    updates = {}

    neighbors = {i: [] for i in range(V)}
    for e in edges:
        neighbors[e[0]].append(e[1])
        neighbors[e[1]].append(e[0])
    for i in range(V):
        dist[i] = {}
        min_dist[i] = {}
        updates[i] = []
        for j in range(V):
            if i == j:
                dist[i][j] = {}
                min_dist[i][j] = 0
                updates[i].append([i, i, 0])
            if i != j:
                dist[i][j] = {}
                min_dist[i][j] = 100000000
                updates[i].append([j, j, 100000000])
        
        for j in range(V):

            for n in neighbors[i]:
                for k in range(V):
                    dist[i][k][n] = 100000000
                for n in neighbors[i]:
                    dist[i][n][n] = 1
                    updates[i].append([n, n, 1])
                
    # iterate
    for iteration in range(V):
        new_updates = {}
        for i in range(V):
            for n in neighbors[i]:
                if n in updates:
                    for u in updates[n]:
                        #print(u)
                        dest = u[0]
                        face = u[1]
                        cost = u[2]
                        if face == i:
                            cost = 100000000
                        dist[i][dest][n] = cost+1
                        if dist[i][dest][n] < min_dist[i][dest]:
                            min_dist[i][dest] = dist[i][dest][n]
                            if i not in new_updates:
                                new_updates[i] = []
                            new_updates[i].append([dest, n, min_dist[i][dest]])
        
        updates = new_updates
    #print(dist)

    # Only use routes to group members
    routes = {}
    for i in range(V):
        routes[i] = {}
        for j in range(V):
            if i != j and j in group_members:
                routes[i][j] = {}
                for d in dist[i][j]:
                    if not dist[i][j][d] > 1000000:
                        routes[i][j][d] = dist[i][j][d]

    return routes

            

def converge(group_members, config_file):
    edges = minindn_to_nodes(config_file)
    all_edges = []
    for e in edges:
        for edge in edges[e]:
            all_edges.append([e, edge])
    nodes = edges.keys()

    V = len(nodes)
    
    all_routes = bellman_ford(V, all_edges, group_members)

    #print(all_routes)

    return nodes, all_routes