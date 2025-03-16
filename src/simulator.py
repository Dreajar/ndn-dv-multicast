from fib import *
from forwarder import *
from pit import *
from rib import *

class Node:
    def __init__(self, nodeID, strategy, simulator):
        self.group_prefixes = []
        self.nodeID = nodeID
        self.pit = Pit(self)
        # Note that the RIB acts as a FIB here
        self.rib = Rib(nodeID)
        self.forwarder = Forwarder(self, strategy)
        self.simulator = simulator
    
    def set_routes(self, routing_info):
        self.rib.set_routes(routing_info)
    
    def add_to_group(self, group_prefix):
        self.group_prefixes.append(group_prefix)

    def receive_interest(self, interest, from_node):
        #self.rib.used_faces.append(from_node)
        return self.pit.receive_interest(interest, from_node)

    def produce_interest(self, prefix):
        return self.pit.produce_interest(prefix)
    
    def get_interest_to_send(self, interestID, face):
        return self.pit.get_interest_to_send(interestID, face)

    def ready_interests(self):
        return self.pit.ready_interests()

class Simulator:
    def __init__(self, num_nodes, strategy):
        self.nodes = [Node(i, strategy, self) for i in range(num_nodes)]
        self.num_nodes = num_nodes
        self.groups = {}
        self.remaining_destinations = {} # This CANNOT be used in forwarding logic, only for metrics
        self.interests_produced = [0 for i in range(num_nodes)]
        self.interests_dropped = [0 for i in range(num_nodes)]
        self.interests_kept = [0 for i in range(num_nodes)]
        self.interests_sent = [0 for i in range(num_nodes)]

    def add_to_group(self, nodeIDs, group_prefix):
        for nodeID in nodeIDs:
            self.nodes[nodeID].add_to_group(group_prefix)
        self.groups[group_prefix] = nodeIDs[::]
    
    def set_routes(self, nodeID, routing_info):
        self.nodes[nodeID].set_routes(routing_info)
    
    def send_interest(self, from_node, face, interestID):
        interest = self.nodes[from_node].get_interest_to_send(interestID, face)
        print(f'Interest {interestID} sent from {from_node} to {face}')
        self.interests_sent[from_node] += 1
        #self.nodes[from_node].rib.used_faces.append(face)
        if face in self.groups[interest.group_prefix]:
            if face in self.remaining_destinations[interestID]:
                self.remaining_destinations[interestID].remove(face)
                if len(self.remaining_destinations[interestID]) == 0:
                    print(f'Interest {interestID} reached all nodes in group!')
        #print(self.remaining_destinations[interestID])
        if not self.nodes[face].receive_interest(interest, from_node):
            print(f'Interest {interestID} dropped at {face}')
            self.interests_dropped[face] += 1
        else:
            self.interests_kept[face] += 1

    def produce_interest(self, node, prefix):
        interest = self.nodes[node].produce_interest(prefix)
        self.remaining_destinations[interest.ID] = [s for s in self.groups[prefix] if s != node]
        #interest.remaining_destinations = [s for s in self.nodes_in_group if s != node]
        self.interests_produced[node] += 1

    def run_forwarding_strategy(self, node):
        return self.nodes[node].forwarder.run_forwarding_strategy()

    def run(self, starting_interests):

        for s in starting_interests:
            nodes = s[0]
            prefix = s[1]
            for node in nodes:
                self.produce_interest(node, prefix)
        while True:
            # Loop until no nodes are sending anything
            interests_sent = [False for i in range(self.num_nodes)]
            for n in self.nodes:
                interests_sent[n.nodeID] = self.run_forwarding_strategy(n.nodeID)
            #print(interests_sent)
            if True not in interests_sent:
                return self.interests_produced, self.interests_dropped, self.interests_kept, self.interests_sent