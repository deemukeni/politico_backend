from api.v2.models import database

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
    def __init__(self, first_name, last_name, username, email, phone_number, passport_url, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.passport_url = passport_url
        self.password = password
        # by default a user is not admin
        # requires to be promoted to be admin
        self.is_admin = False

    def create_user(self):

        query = """
        INSERT INTO users(firstname, lastname, username, email, password, phoneNumber, passport_url) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.first_name, self.last_name, self.username, self.email, self.password, self.phone_number, self.passport_url )
        

        database.insert_to_db(query)

    @classmethod
    def get_user_by_phone_number(cls, phone_number):

        query = """
        SELECT phoneNumber FROM users WHERE users.phoneNumber = '{}'
        """.format(phone_number)

        phone = database.select_from_database(query)
        return phone

    @classmethod
    def  get_user_by_username(cls, username):

        query = """
        SELECT * FROM users WHERE users.username = '{}'
        """.format(username)

        user = database.select_from_database(query)
        # try:
        #     user = user[0][1]

        #     print(user)
        # except:
        #     print("No user posted yet")
        return user

    @classmethod
    def  get_user_by_email(cls, email):

        query = """
        SELECT email FROM users WHERE users.email = '{}'
        """.format(email)

        email = database.select_from_database(query)
        return email

    @staticmethod
    def get_user_by_password(password):

        query = """
        SELECT password FROM users WHERE users.password = '{}'
        """.format(password)

        password = database.select_from_database(query)
        return password
    
    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username":  self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "passport_url": self.passport_url
            
        }
