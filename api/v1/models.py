# store app models
# a list of party objects
PARTIES = []

class Party:
    def __init__(self, name, hqaddress, logo_url):
        self.id = len(PARTIES) + 1
        self.name = name
        self.hqaddress = hqaddress
        self.logo_url = logo_url
    
    def create_party(self):
        # save party to store
        PARTIES.append(self)
        print("PARTIES => ", PARTIES)
    
    @classmethod
    def get_party_by_name(cls, name):
        for party in PARTIES:
            if party.name == name:
                return party
        return None

    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "name": self.name,
            "hqaddress": self.hqaddress,
            "logo_url": self.logo_url
        }
