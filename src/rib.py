class Rib:
    def __init__(self, nodeID):
        self.nodeID = nodeID
        self.faces = []
        self.routes = {}
    
    def set_routes(self, routing_info):
        # Takes the place of actually creating the routing algorithm, temporarily
        for node in routing_info:
            for face in routing_info[node]:
                if face not in self.faces:
                    self.faces.append(face)
                if node not in self.routes:
                    self.routes[node] = {}
                self.routes[node][face] = routing_info[node][face]
    
    def get_lowest_cost_routes(self, node):
        # Gets the lowest cost route to a node.
        #print(node, used_faces, self.routes)
        lowest_cost = 10000000000
        lowest_cost_nodes = []
        for f in self.routes[node]:
            if self.routes[node][f] < lowest_cost:
                lowest_cost = self.routes[node][f]

        for f in self.routes[node]:
            if self.routes[node][f] == lowest_cost:
                lowest_cost_nodes.append(self.routes[node][f])
        return lowest_cost_nodes
            
    def get_all_faces_to_node(self, node):
        # Returns all faces that can reach a node and have not yet been used by an interest
        if node not in self.routes:
            return []
        for f in self.routes[node]:
            return [s for s in self.routes[node].keys()]
