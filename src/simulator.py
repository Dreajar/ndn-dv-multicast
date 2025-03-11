from fib import *
from forwarding_strategies import *
from pit import *
from rib import *

STRATEGY_LOWEST_COST = 1
STRATEGY_SEND_ALL = 2

strategy_names = {1: "lowest_cost", 2: "send_all"}

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

    def receive_interest(self, interest):
        return self.pit.receive_interest(interest)

    def produce_interest(self):
        return self.pit.produce_interest()
    
    def get_interest_to_send(self, interestID, face):
        return self.pit.get_interest_to_send(interestID, face)

    def ready_interests(self):
        return self.pit.ready_interests()

class Simulator:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.num_nodes = num_nodes
        self.nodes_in_group = []
        self.interests_produced = [0 for i in range(num_nodes)]
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
        print(f'Interest {interestID} sent from {from_node} to {face}')
        interest = self.nodes[from_node].get_interest_to_send(interestID, face)
        if face in self.nodes_in_group:
            if face in interest.remaining_destinations:
                interest.remaining_destinations.remove(face)
                if len(interest.remaining_destinations) == 0:
                    print(f'Interest {interestID} reached all nodes in group!')
        if not self.nodes[face].receive_interest(interest):
            self.interests_dropped[face] += 1

    def produce_interest(self, node):
        interest = self.nodes[node].produce_interest()
        interest.remaining_destinations = [s for s in self.nodes_in_group if s != node]
        self.interests_produced[node] += 1

    def run_forwarding_strategy(self, strategy, node):
        if strategy == STRATEGY_LOWEST_COST:
            any_sent = False
            for interestID in self.nodes[node].ready_interests():
                used_faces = self.nodes[node].pit.used_faces_by_interest(interestID)
                faces_to_send = []
                for n in self.nodes[node].pit.get_interest_by_id(interestID).remaining_destinations:
                    if n != node:
                        lowest_cost_face = self.nodes[node].rib.get_lowest_cost_route(n, used_faces)
                        if lowest_cost_face not in faces_to_send:
                            faces_to_send.append(lowest_cost_face)

                for f in faces_to_send:
                    any_sent = True
                    self.interests_sent[node] += 1
                    self.interests_received[f] += 1
                    self.send_interest(node, f, interestID)
            return any_sent

        if strategy == STRATEGY_SEND_ALL:
            any_sent = False
            for interestID in self.nodes[node].ready_interests():
                used_faces = self.nodes[node].pit.used_faces_by_interest(interestID)
                faces_to_send = []
                for n in self.nodes[node].pit.get_interest_by_id(interestID).remaining_destinations:
                    if n != node:
                        possible_faces = self.nodes[node].rib.get_all_faces_to_node(n)
                        for p in possible_faces:
                            if p not in faces_to_send:
                                faces_to_send.append(p)

                for f in faces_to_send:
                    any_sent = True
                    self.interests_sent[node] += 1
                    self.interests_received[f] += 1
                    self.send_interest(node, f, interestID)
            return any_sent



    def run(self, strategy, starting_interests):
        for s in starting_interests:
            self.produce_interest(s)
        while True:
            # Loop until no nodes are sending anything
            interests_sent = [False for i in range(self.num_nodes)]
            for n in self.nodes:
                interests_sent[n.nodeID] = self.run_forwarding_strategy(strategy, n.nodeID)
            if True not in interests_sent:
                return self.interests_produced, self.interests_dropped, self.interests_received, self.interests_sent