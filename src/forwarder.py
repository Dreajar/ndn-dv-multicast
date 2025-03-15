STRATEGY_LOWEST_COST = 1
STRATEGY_SEND_ALL = 2

class StrategySendAll:
    name = "send_all"
    def __init__(self, forwarder):
        self.forwarder = forwarder

    def on_receive(self, interest, face):
        return face in self.forwarder.node.rib.get_lowest_cost_routes(interest.producer)

    def choose_interests_to_send(self):
        interests_to_send = []
        for interestID in self.forwarder.interests():
            #print(self.forwarder.all_faces(), self.forwarder.in_faces())
            faces_to_send = [s for s in self.forwarder.all_faces() if s not in self.forwarder.in_faces()[interestID]]
            interest_and_faces = (interestID, faces_to_send)
            interests_to_send.append(interest_and_faces)
        #print(self.forwarder.node.nodeID, interests_to_send)
        return interests_to_send



class StrategyLowestCost:
    name = "lowest_cost"
    def __init__(self, forwarder):
        self.forwarder = forwarder

    def on_receive(self, interest, face):
        return face in self.forwarder.node.rib.get_lowest_cost_routes(interest.producer)

    def choose_interests_to_send(self):
        interests_to_send = []
        for interestID in self.forwarder.interests():
            #self.forwarder.interests()[interestID]
            faces_to_send = [s for s in self.forwarder.all_faces() if s not in self.forwarder.in_faces()[interestID]]
            interest_and_faces = (interestID, faces_to_send)
            interests_to_send.append(interest_and_faces)

        return interests_to_send


strategy_map = {STRATEGY_LOWEST_COST: StrategyLowestCost, STRATEGY_SEND_ALL: StrategySendAll}

class Forwarder:
    def __init__(self, node, strategy): # Strategy will be set by simulator
        self.node = node
        self.strategy = strategy(self) # Instantiate forwarding strategy from list

    def interests(self):
        return self.node.pit.interests
    
    # These two return maps of interestID to faces
    def in_faces(self):
        return self.node.pit.in_faces
    
    def out_faces(self):
        return self.node.pit.out_faces

    # This just returns a list of all faces
    def all_faces(self):
        return self.node.rib.faces

    def on_receive(self, interest, face):
        return self.strategy.on_receive(interest, face)

    def run_forwarding_strategy(self):
        for interest_and_faces in self.strategy.choose_interests_to_send():
            interestID = interest_and_faces[0]
            faces = interest_and_faces[1]
            for f in faces:
                self.node.simulator.send_interest(self.node.nodeID, f, interestID)