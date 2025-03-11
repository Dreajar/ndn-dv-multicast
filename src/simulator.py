from fib import *
from forwarding_strategies import *
from pit import *
from rib import *

STRATEGY_LOWEST_COST = 1

class Node:
    def __init__(self, nodeID):
        self.in_group = False
        self.nodeID = nodeID
        self.pit = Pit()
        # Note that the RIB acts as a FIB here
        self.rib = Rib(nodeID)
        self.faces = []

    def set_faces(self, faces):
        self.faces = faces
    
    def set_routes(self, routing_info):
        self.rib.set_routes(routing_info)
    
    def add_to_group(self):
        self.in_group = True

    def add_interest(self, interest):
        self.pit.add_interest(interest)
    
    def get_interest_to_send(self, interestID, face):
        return self.pit.get_interest_to_send(interestID, face)

    def ready_interests(self):
        return self.pit.ready_interests()

class Simulator:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.num_nodes = num_nodes
        self.nodes_in_group = []
        self.interests_dropped = [0 for i in range(num_nodes)]
        self.interests_received = [0 for i in range(num_nodes)]
        self.interests_sent = [0 for i in range(num_nodes)]

    def add_to_group(self, nodeIDs):
        for nodeID in nodeIDs:
            self.nodes[nodeID].add_to_group()
            self.nodes_in_group.append(nodeID)
    
    def set_routes(self, nodeID, routing_info):
        self.nodes[nodeID].set_routes(routing_info)
    
    def send_interest(self, from_node, face, interestID):
        interest = self.nodes[from_node].get_interest_to_send(interestID, face)
        self.nodes[face].add_interest(interest)

    def add_interest(self, node):
        interest = Interest()
        if not self.nodes[node].add_interest(interest):
            self.interests_dropped[node] += 1

    def run_forwarding_strategy(self, strategy, node):
        if strategy == STRATEGY_LOWEST_COST:
            any_sent = False
            for interestID in self.nodes[node].ready_interests():
                used_faces = self.nodes[node].pit.used_faces_by_interest(interestID)
                faces_to_send = []
                for n in self.nodes_in_group:
                    if n != node:
                        lowest_cost_face = self.nodes[node].rib.get_lowest_cost_route(n, used_faces)
                        if lowest_cost_face not in faces_to_send:
                            faces_to_send.append(lowest_cost_face)

                for f in faces_to_send:
                    any_sent = True
                    self.interests_sent[node] += 1
                    self.interests_received[node] += 1
                    self.send_interest(node, f, interestID)
            return any_sent



    def run(self, strategy, starting_interests):
        for s in starting_interests:
            self.add_interest(s)
        while True:
            # Loop until no nodes are sending anything
            interests_sent = [False for i in range(self.num_nodes)]
            for n in self.nodes:
                interests_sent[n.nodeID] = self.run_forwarding_strategy(strategy, n.nodeID)
            if True not in interests_sent:
                return self.interests_dropped, self.interests_received, self.interests_sent