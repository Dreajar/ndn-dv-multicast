INTEREST_STATE_READY = 1
INTEREST_STATE_SENT = 2


class Interest:
    nextIntID = 1

    def __init__(self, original=None):
        if original == None:
            self.ID = Interest.nextIntID
            Interest.nextIntID += 1
            self.remaining_destinations = []
            self.used_faces = []
        else:
            self.ID = original.ID
            self.remaining_destinations = original.remaining_destinations[::]
            self.used_faces = original.used_faces[::]
        self.state = INTEREST_STATE_READY


class Pit:
    def __init__(self, nodeID):
        self.nodeID = nodeID
        self.interests = {}
        self.IDs = []
        self.ready_IDs = []
        self.sent_IDs = []
    
    def receive_interest(self, interest):
        # If an interest arrives that has already been sent, ready to send it again
        if interest.ID not in self.ready_IDs:
            self.ready_IDs.append(interest.ID)
            if interest.ID in self.IDs:
                self.interests[interest.ID].state = INTEREST_STATE_READY
        # Returns False if the packet is dropped
        if interest.ID in self.interests:
            return False
        self.interests[interest.ID] = interest
        self.IDs.append(interest.ID)
        return True
    
    def produce_interest(self):
        interest = Interest()
        interest.used_faces.append(self.nodeID)
        # If an interest arrives that has already been sent, ready to send it again
        self.ready_IDs.append(interest.ID)
        self.IDs.append(interest.ID)
        interest.state = INTEREST_STATE_READY
        self.interests[interest.ID] = interest

        # Returns the actual interest instead of a copy - be careful!
        return interest

    def used_faces_by_interest(self, interestID):
        return self.interests[interestID].used_faces

    def has_interest(self, interestID):
        return interestID in self.IDs

    def ready_interests(self):
        return self.ready_IDs
    
    def use_face(self, face, interestID):
        self.interests[interestID].used_faces.append(face)

    def get_interest_by_id(self, interestID):
        return Interest(original=self.interests[interestID])

    def get_interest_to_send(self, interestID, face):
        if interestID in self.ready_IDs:
            self.ready_IDs.remove(interestID)
            self.sent_IDs.append(interestID)
            self.interests[interestID].state = INTEREST_STATE_SENT
        return Interest(original=self.interests[interestID])