# store app models
# a list of party objects
PARTIES = []
# list of all available offices that were created
OFFICES = []
#list of all users
USERS = []

class Party:
    def __init__(self, name, hqaddress, logo_url):
        self.id = len(PARTIES) + 1
        self.name = name
        self.hqaddress = hqaddress
        self.logo_url = logo_url
    
    def create_party(self):
        # save party to store
        PARTIES.append(self)
    
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

class User:
    def __init__(self, first_name, last_name, other_name, email, phone_number, passport_url):
        self.id = len(USERS) + 1
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.email = email
        self.phone_number = phone_number
        self.passport_url = passport_url
        # by default a user is not admin
        # requires to be promoted to be admin
        self.is_admin = False

    def create_user(self):
        USERS.append(self)

    @classmethod
    def get_user_by_phone_number(cls, phone_number):
        for user in USERS:
            if user.phone_number == phone_number:
                return user
        return None

    @classmethod
    def  get_user_by_email(cls, email):
        for user in USERS:
            if user.email == email:
                return user
        return None

    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "other_name":  self.other_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "passport_url": self.passport_url
            
        }
