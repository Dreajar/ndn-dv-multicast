INTEREST_STATE_READY = 1
INTEREST_STATE_SENT = 2


class Interest:
    nextIntID = 1

    def __init__(self, original=None):
        if original == None:
            self.ID = Interest.nextIntID
            Interest.nextIntID += 1
        else:
            self.ID = original.ID
        self.used_faces = []
        self.state = INTEREST_STATE_READY


class Pit:
    def __init__(self):
        self.interests = {}
        self.IDs = []
        self.ready_IDs = []
        self.sent_IDs = []
    
    def add_interest(self, interest):
        # Returns False if the packet is dropped
        if interest.ID in self.interests:
            return False
        self.interests[interest.ID] = interest
        self.IDs.append(interest.ID)
        self.ready_IDs.append(interest.ID)
        interest.state = INTEREST_STATE_READY
        return True

    def used_faces_by_interest(self, interestID):
        return self.interests[interestID].used_faces

    def has_interest(self, interestID):
        return interestID in self.IDs

    def ready_interests(self):
        return self.ready_IDs

    def get_interest_by_id(self, interestID):
        return Interest(original=self.interests[interestID])

    def get_interest_to_send(self, interestID, face):
        self.ready_IDs.remove(interestID)
        self.sent_IDs.append(interestID)
        self.interests[interestID].state = INTEREST_STATE_SENT
        return Interest(original=self.interests[interestID])