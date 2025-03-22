STRATEGY_LOWEST_COST = 1
STRATEGY_SEND_ALL = 2

class StrategySendAll:
    name = "send_all"
    def __init__(self, forwarder):
        self.forwarder = forwarder

    def on_receive(self, interest, face):
        is_lowest_cost_route = face in self.forwarder.node.rib.get_lowest_cost_routes(interest.producer)
        already_have = interest.ID in self.forwarder.interests()
        return is_lowest_cost_route and not already_have

    def choose_interests_to_send(self):
        interests_to_send = []
        for interestID in self.forwarder.interests():
            in_faces = [] if interestID not in self.forwarder.in_faces() else self.forwarder.in_faces()[interestID]
            out_faces = [] if interestID not in self.forwarder.out_faces() else self.forwarder.out_faces()[interestID]
            faces_to_send = [s for s in self.forwarder.all_faces() if s not in in_faces and s not in out_faces]
            interest_and_faces = (interestID, faces_to_send)
            interests_to_send.append(interest_and_faces)
        return interests_to_send



class StrategyLowestCost:
    name = "lowest_cost"
    def __init__(self, forwarder):
        self.forwarder = forwarder

    def on_receive(self, interest, face):
        is_lowest_cost_route = face in self.forwarder.node.rib.get_lowest_cost_routes(interest.producer)
        already_have = interest.ID in self.forwarder.interests()
        return is_lowest_cost_route and not already_have

    def choose_interests_to_send(self):
        interests_to_send = []
        for interestID in self.forwarder.interests():
            in_faces = [] if interestID not in self.forwarder.in_faces() else self.forwarder.in_faces()[interestID]
            out_faces = [] if interestID not in self.forwarder.out_faces() else self.forwarder.out_faces()[interestID]
            faces_to_send = [s for s in self.forwarder.node.rib.get_all_best_routes() if s not in in_faces and s not in out_faces]
            interest_and_faces = (interestID, faces_to_send)
            interests_to_send.append(interest_and_faces)

        return interests_to_send


strategy_map = {STRATEGY_SEND_ALL: StrategySendAll, STRATEGY_LOWEST_COST: StrategyLowestCost}

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

    # The on_receive function in each strategy returns whether to drop the packet or not
    def on_receive(self, interest, face):
        return self.strategy.on_receive(interest, face)

    # Sends all interests available, returns whether any were sent
    def run_forwarding_strategy(self):
        any_sent = False
        for interest_and_faces in self.strategy.choose_interests_to_send():
            interestID = interest_and_faces[0]
            faces = interest_and_faces[1]
            for f in faces:
                self.node.simulator.send_interest(self.node.nodeID, f, interestID)
                any_sent = True
        return any_sent