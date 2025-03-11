class Route:
    def __init__(self, faceID, origin):
        # Assume cost over all links is 1 for simplicity
        self.faceID = faceID
        self.origin = origin


class Rib:
    def __init__(self, nodeID):
        self.nodeID = nodeID
        self.faces = []
        self.routes = {}
    
    def set_routes(self, routing_info):
        # Takes the place of actually creating the routing algorithm, temporarily
        for node in routing_info:
            for face in routing_info[node]:
                if node not in self.routes:
                    self.routes[node] = {}
                self.routes[node][face] = routing_info[node][face]
    
    def get_lowest_cost_route(self, node, used_faces):
        # Gets the lowest cost route to a node.
        #print(node, used_faces, self.routes)
        lowest_cost = 10000000000
        lowest_cost_node = -1
        for f in self.routes[node]:
            if f in used_faces:
                continue
            if self.routes[node][f] < lowest_cost:
                lowest_cost = self.routes[node][f]
                lowest_cost_node = f
        return lowest_cost_node
            
    def get_all_faces_to_node(self, node, used_faces=[]):
        # Returns all faces that can reach a node and have not yet been used by an interest
        if node not in self.routes:
            return []
        if node in used_faces:
            return []
        for f in self.routes[node]:
            return [s for s in self.routes[node].keys() if s not in used_faces]
