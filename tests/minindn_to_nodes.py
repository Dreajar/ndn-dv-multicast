import sys


# This file is to be used if you want to test with a pre-created minindn topology (for example, the sprint topology)
def minindn_to_nodes(config_file):
    f = open(config_file, 'r')
    lines = f.readlines()

    state = "initial"
    nodeID = 0
    node_to_ID = {}

    edges = {}

    for line in lines:
        if state == 'initial':
            if line.strip() == '[nodes]':
                state = 'nodes'
        elif state == 'nodes':
            if line.strip() == '[links]':
                state = 'links'
            elif line.find(':') != -1:
                node_name = line[:line.find(':')]
                node_to_ID[node_name] = nodeID
                edges[nodeID] = []
                nodeID += 1
        elif state == 'links':
            node1 = line[:line.find(':')]
            node2 = line[line.find(':')+1:line.find(' ')]
            edges[node_to_ID[node1]].append(node_to_ID[node2])
            edges[node_to_ID[node2]].append(node_to_ID[node1])

    return edges





if __name__ == '__main__':
    print(minindn_to_nodes(sys.argv[1]))