import datetime

from api.v2.models.database import QueryDatabase
import psycopg2

class Party:
    def __init__(self, name, hqaddress, logo_url):
        self.name = name
        self.hqaddress = hqaddress
        self.logo_url = logo_url
    
    def create_party(self):
        """
        A method to create a party.
        :param name: A string, the party's name.
        :param hqaddress: A varchar, the party's address.
        :param logo_url: A varchar, the party's link to it's logo.
        """
        query = """
        INSERT INTO parties(party_name, hqAddress, logo_url) VALUES(
            '{}', '{}', '{}')
        """.format(self.name, self.hqaddress, self.logo_url)
    
        QueryDatabase.insert_to_db(query)

    @classmethod
    def get_party_by_name(cls, name):
        """
        pick a party created from the table in database by its name since its a 
        unique identifier of the party
        parameter: name: party name.
        return: the party whose name has been requested
        """
        query = """
        SELECT * FROM parties WHERE party_name='{}'
        """.format(name)
        user = QueryDatabase.select_from_database(query)
        return user

    @classmethod
    def get_all_parties(cls):
        """
        Get all available parties from  the table in database
        returns: a list of the available parties
        """
        query="""
        SELECT * FROM parties
        """
        parties = QueryDatabase.select_from_database(query)
        parties_lst = []
        for party in parties:
            # convert party tuple to a dictionary - which is easily jsonified
            parties_lst.append(Party.to_json(party))
        return parties_lst

    @classmethod
    def get_party_by_id(cls, id):
        """
        A method to get a specific party by id
        :param id: the party id
        :return: the party matching the id if found otherwise none
        """

        query=""" SELECT * FROM parties WHERE party_id='{}'
        """.format(id)
        party = QueryDatabase.select_from_database(query)
        try:
            party = Party.to_json(party[0])
        except:
            print("no party yet")
        return party

    @staticmethod
    def update_party(party_name, hqaddress, logo_url, party_id):
        """
        Docstring
        """
        query = """
        UPDATE parties SET party_name = '{}', hqaddress = '{}', logo_url = '{}' WHERE parties.party_id = '{}'
        """.format(party_name, hqaddress, logo_url, party_id)

        QueryDatabase.insert_to_db(query)


    @classmethod
    def delete_party(cls, id):
        """
        A method to delete a party.
        param id: id of the party that is to be deleted
        """

        party = Party.get_party_by_id(id)

        if party:
            query="""
            DELETE FROM parties WHERE parties.party_id='{}' 
            """.format(id)
            QueryDatabase.insert_to_db(query)
      

    @classmethod
    def to_json(self, party_row):
        """
        convert from object to dictionary for easy rendering as json responseget_party_by_id
        :return:parameters in json format
        
        """
        return {
            "id": party_row[0],
            "name": party_row[1],
            "hqaddress": party_row[2],
            "logo_url": party_row[3]
        }


class Office:
    def __init__(self, office_type, name):
        self.office_type = office_type
        self.name =name
    
    def create_office(self):
        """
        A method to create an office.
        :param name: A string, the office name.
        :param hqaddress: A varchar, the office address.
        :param logo_url: A varchar, the office link to it's logo.
        :return: Office created successfully.
        """
        query = """
        INSERT INTO offices(office_type, office_name) VALUES(
            '{}', '{}')
        """.format(self.office_type, self.name)
        QueryDatabase.insert_to_db(query)

    @classmethod
    def get_office_by_name(cls, name):
        """
        Get a specific  office  from the table in database by its id "/office/name"
        :return: specific office querried
        """
        query = """
        SELECT * FROM offices WHERE office_name='{}'
        """.format(name)
        user = QueryDatabase.select_from_database(query)
        return user


    @classmethod
    def get_all_offices(cls):
        """
        Get all available offices from  the table in database
        :return: all offices available in the database
        """
        query="""
        SELECT * FROM offices
        """
        offices = QueryDatabase.select_from_database(query)
        offices_lst = []
        for office in offices:
            # convert party tuple to a dictionary - which is easily jsonified
            offices_lst.append(Office.to_json(office))
        return offices_lst


    @classmethod
    def get_office_by_id(cls, id):
        """
        Get a specific  office  from the table in database by its id"/parties/<int:id>"
        :param id: office id    
        :return: requested office
        """
        query=""" SELECT * FROM offices WHERE office_id='{}'
        """.format(id)
        office = QueryDatabase.select_from_database(query)
        try:
            office = Office.to_json(office[0])
        except:

            print("No office found")
        return office

    @staticmethod
    def update_office(office_name, office_type, office_id):
        """
        Docstring
        """
        query = """
        UPDATE offices SET office_name = '{}', office_type = '{}' WHERE offices.office_id = '{}'
        """.format(office_name, office_type, office_id)

        QueryDatabase.insert_to_db(query)

    @classmethod
    def delete_office(cls, id):
        """
        Remove a specific  office  from the table in database.
        :param id: the office id
        """
        office = Office.get_office_by_id(id)
        if office:
            query="""
            DELETE FROM offices WHERE offices.office_id='{}' 
            """.format(id)
            QueryDatabase.insert_to_db(query)
    


    @classmethod
    def to_json(self, office_row):
        """
        convert from object to dictionary for easy rendering as json response
        :return: the  available data in json format
        """
        return {
            "office_id": office_row[0],
            "office_type": office_row[1],
            "office_name": office_row[2]
        }

class User:
    def __init__(self, first_name, last_name, username, email, phone_number, passport_url, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.passport_url = passport_url
        self.password = password
        self.role = role
        # by default a user is not admin
        # requires to be promoted to be admin
        self.is_admin = False

    def create_user(self):
        """
        Add a new user to the database
        Queries the database to add data into the users table
        """

        query = """
        INSERT INTO users(firstname, lastname, username, email, password, phoneNumber, passport_url, role) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.first_name, self.last_name, self.username, self.email, self.password, self.phone_number, self.passport_url, self.role )

        QueryDatabase.insert_to_db(query)

    @classmethod
    def get_user_by_phone_number(cls, phone_number):
        """
        Query database to get a user by their phone number
        :return: user with the phone number used
        """

        query = """
        SELECT * FROM users WHERE users.phoneNumber='{}'
        """.format(phone_number)

        user = QueryDatabase.select_from_database(query)
        return user

    @classmethod
    def  get_user_by_username_and_password(cls, username, password):
        """
        Get a user by their username
        :params: user's username
        :return: user with requested username
        """

        query = """
        SELECT * FROM users WHERE username='{}' AND password='{}'
        """.format(username, password)

        user = QueryDatabase.select_from_database(query)
        return user

    @classmethod
    def  get_user_by_username(cls, username):
        """
        Get a user by their username
        :params: user's username
        :return: user with requested username
        """

        query = """
        SELECT * FROM users WHERE username='{}'
        """.format(username)

        user = QueryDatabase.select_from_database(query)
        return user


    @classmethod
    def  get_user_by_email(cls, email):
        """
        Get a user by their email
        :param email: user's email
        :return: user whose email was querried
        """

        query = """
        SELECT email FROM users WHERE users.email='{}'
        """.format(email)

        email = QueryDatabase.select_from_database(query)
        return email

    @staticmethod
    def get_user_by_password(password):
        """
        Used to verify the correct username-passwword combination
        :param password: user's password
        :return: password
        """

        query = """
        SELECT password FROM users WHERE users.password='{}'
        """.format(password)

        password = QueryDatabase.select_from_database(query)
        return password
    
    def to_json(self, user_row):
        """
        convert from object to dictionary for easy rendering as json response
        :return: the  available data in json format
        """
        return {
            "id": user_row[0],
            "first_name": user_row[1],
            "last_name": user_row[2],
            "username":  user_row[3],
            "email": user_row[4],
            "phone_number": user_row[6],
            "passport_url": user_row[7],
            "role": user_row[7]
        }

class Candidates:
    def __init__(self, id, candidate_name, office_id, party_id):
        self.candidate_name = candidate_name
        self.office_id = office_id
        self.party_id = party_id

    def create_candidate():
        """
        Creates a candidate
        """
        query = """
        INSERT INTO candidates(candidate_name, office_id, party_id) VALUES(
            '{}', '{}', '{}'
        )""".format(self.candidate_name, self.office_id, self.party_id)
        QueryDatabase.insert_to_db(query)


    def does_candidate_exist(candidate_id, office_id):
        """
        Checks if candidate exists in database
        :params candidate_id: id of the candidate
        :params office_id: id of office that the candidate is running for
        :return: candidate
        """
        query = """
        SELECT candidate_name, office_id FROM candiddates WHERE candidates.candidate_name AND candidates.office_id VALUES(
            '{}', '{}'
        )""".format(self.candidate_name, self.office_id)

        candidate= QueryDatabase.select_from_db(query)
        return candidate


    def add_candidate_to_database():
        """
        Adds a new candidate to the database
        """
        query = """
        INSERT INTO candidates(candidate_name, office_id) VALUES(
            '{}', '{}'
        )""".format(self.candidate_name, self.office_id)
        QueryDatabase.insert_to_db(query)

    


    def to_json(self):
        """
        convert from object to dictionary for easy rendering as json response
        :return: the  available data in json format
        """
        return {
            "id": user_row[0],
            "candidate_name": user_row[1],
            "office_id": user_row[2],
            "party_id":  user_row[3],
        }

class Votes:
    def __init__(self, createBy, candidateVoteFor, officeVotedFor):
        self.createdOn = datetime.datetime.utcnow()
        self.createBy = createBy
        self.candidateVoteFor = candidateVoteFor
        self.officeVotedFor = officeVotedFor

    def create_vote(self):
        """
        Creates a vote
        :param officeVotedFor: office that the candidate is running for
        :param createBy: voter
        :param candidateVoteFor: candidate voted for
        :param createdOn: date of vote
        """
        query = """
        INSERT INTO votes(createdOn, createBy, candidateVoteFor, officeVotedFor) VALUES(
            '{}', '{}', '{}', '{}'
        )""".format(self.createdOn, self.createBy, self.candidateVoteFor, self.officeVotedFor)
        

        QueryDatabase.insert_to_db(query)

    def check_that_user_has_voted(created_by, officeVotedFor):
        """
        """
        query = """
        SELECT createdBy, officeVotedFor FROM votes WHERE
        votes.createdBy = '{}' AND votes.officeVotedFor = '{}'
        """.format(created_by, officeVotedFor)

        voted = QueryDatabase.insert_to_db(query)
        return voted


    def user_vote():
        query="""
        SELECT createdBy, officeVotedFor FROM votes WHERE votes.createdBy='{}'  AND votes.officeVotedFor='{}'""".format(createdBy,officeVotedFor)
    def to_json(self):
        """
        convert from object to dictionary for easy rendering as json response
        :return: the  available data in json format
        """
        return {
            "id": user_row[0],
            "createdOn": user_row[1],
            "createBy": user_row[2],
            "candidateVoteFor":  user_row[3],
            "officeVotedFor": user_row[4]
        }
        
# def results():
#     """
#         """
#         query = """
#         SELECT offices.office_id candidates.candidate_id

#         voted = QueryDatabase.insert_to_db(query)
#         return voted
