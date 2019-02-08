# store app models
# a list of party objects
PARTIES = []
# list of all available offices that were created
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
        #loop through the PARTIES
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
    def __init__(self, office_type, name):
        self.id = len(OFFICES) + 1
        self.office_type = office_type
        self.name =name
    
    def create_office(self):
        OFFICES.append(self)
        print("Offices: ", OFFICES )

    @classmethod
    def get_office_by_name(cls, name):
        #loop through the PARTIES
        for office in OFFICES:
            if office.name == name:
                return office
        return None


    @classmethod
    def get_all_offices(cls):
        offices = []
        for office in OFFICES:
            offices.append(office.to_json())
        return offices

    @classmethod
    def get_office_by_id(cls , id):
        single_office = None
        for office in OFFICES:
            if office.id == id:
                single_office = office
                break
        return single_office

    @classmethod
    def delete_office(cls, id):
        office = Office.get_office_by_id(id)
        OFFICES.remove(office)
    



    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "office_type": self.office_type,
            "name": self.name
        }
