INTEREST_STATE_READY = 1
INTEREST_STATE_SENT = 2

PRODUCED_INTEREST = -1


class Interest:
    nextIntID = 1

    # Call this with one of (producer and group_prefix) or original, not both and not neither
    def __init__(self, producer="", group_prefix="", original=None):
        if original == None:
            self.ID = Interest.nextIntID
            Interest.nextIntID += 1
            self.group_prefix = group_prefix
            self.producer = producer
        else:
            self.ID = original.ID
            self.group_prefix = original.group_prefix
            self.producer = original.producer


class Pit:
    def __init__(self, node):
        self.node = node
        self.nodeID = node.nodeID
        self.interests = {}
        self.IDs = []
        self.ready_IDs = []
        self.sent_IDs = []
        self.in_faces = {}
        self.out_faces = {}
    
    def receive_interest(self, interest, face):
        # If an interest arrives that has already been sent, ready to send it again
        if interest.ID not in self.in_faces:
            self.in_faces[interest.ID] = []
        self.in_faces[interest.ID].append(face)

        if not self.node.forwarder.on_receive(interest, face):
            return False

        if interest.ID not in self.ready_IDs:
            self.ready_IDs.append(interest.ID)
        # Returns False if the packet is dropped
        self.interests[interest.ID] = interest
        self.IDs.append(interest.ID)
        return True
    
    def produce_interest(self, group_prefix):
        interest = Interest(producer=self.nodeID, group_prefix=group_prefix)
        # If an interest arrives that has already been sent, ready to send it again
        self.ready_IDs.append(interest.ID)
        self.IDs.append(interest.ID)
        self.interests[interest.ID] = interest

        self.in_faces[interest.ID] = [PRODUCED_INTEREST] # means the interest was created here, so not received from another interface

        # Returns the actual interest instead of a copy - be careful!
        return interest

    def has_interest(self, interestID):
        return interestID in self.IDs

    def ready_interests(self):
        return self.ready_IDs

    def get_interest_by_id(self, interestID):
        return Interest(original=self.interests[interestID])

    def get_interest_to_send(self, interestID, face):
        if interestID not in self.out_faces:
            self.out_faces[interestID] = []
        self.out_faces[interestID].append(face)
        if interestID in self.ready_IDs:
            self.ready_IDs.remove(interestID)
            self.sent_IDs.append(interestID)
        return Interest(original=self.interests[interestID])