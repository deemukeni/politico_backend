# store app models
# a list of party objects
PARTIES = []
OFFICES = []

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

    @classmethod
    def get_all_parties(cls):
        parties = []
        for party in PARTIES:
            # store as dictionaries
            parties.append(party.to_json())
        return parties
    
    @classmethod
    def get_party_by_id(cls, id):
        single_party = None
        for party in PARTIES:
            if party.id == id:
                single_party = party
                break
        return single_party

    """
    add patch endpoint to update a party by id
        dont forget!!!!!
    """

    @classmethod
    def delete_party(cls, id):
        """
        update a political party
        """
        party = Party.get_party_by_id(id)
        PARTIES.remove(party)

    
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


class Office:
    def __init__(self, officetype, name):
        self.id = id
        self.officetype = officetype
        self.name =name
    
    
    def create_office(self):
        OFFICES.append(self)
        print("Offices: ", OFFICES )


    # @classmethod
    # def get_all_offices():


    
    
    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "officetype": self.officetype,
            "name": self.name,
            
        }

    
