import datetime

from api.v2.models import database
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
        :return: Party created successfully.
        """
        query = """
        INSERT INTO parties(party_name, hqAddress, logo_url) VALUES(
            '{}', '{}', '{}')
        """.format(self.name, self.hqaddress, self.logo_url)
    
        database.insert_to_db(query)

    @classmethod
    def get_party_by_name(cls, name):
        """
        pick a party created from the table in database by its name since its a 
        unique identifier of the party
        parameter: name
        """
        query = """
        SELECT * FROM parties WHERE party_name='{}'
        """.format(name)
        user = database.select_from_database(query)
        return user

    @classmethod
    def get_all_parties(cls):
        """
        Get all available parties from  the table in database
        """
        query="""
        SELECT * FROM parties
        """
        parties = database.select_from_database(query)
        parties_lst = []
        for party in parties:
            # convert party tuple to a dictionary - which is easily jsonified
            parties_lst.append(Party.to_json(party))
        return parties_lst

    @classmethod
    def get_party_by_id(cls, id):
        """
        Get a specific  party  from the table in database by its id
        "/parties/<int:id>"
        """
        query=""" SELECT * FROM parties WHERE party_id='{}'
        """.format(id)
        party = database.select_from_database(query)
        try:
            party = Party.to_json(party[0])
        except:
            print("no party yet")
        return party


    @classmethod
    def delete_party(cls, id):
        """
        delete a political party from the database
        """
        party = Party.get_party_by_id(id)

        if party:
            query="""
            DELETE FROM parties WHERE parties.party_id='{}' 
            """.format(id)
            try:
                conn, cursor = database.connect_db()
                cursor.execute(query)
                conn.commit()
                conn.close()
            except psycopg2.Error as error:
                print (error)

      

    @classmethod
    def to_json(self, party_row):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
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
        database.insert_to_db(query)

    @classmethod
    def get_office_by_name(cls, name):
        """
        Get a specific  office  from the table in database by its id
        "/office/name"
        """
        query = """
        SELECT * FROM offices WHERE office_name='{}'
        """.format(name)
        user = database.select_from_database(query)
        return user


    @classmethod
    def get_all_offices(cls):
        """
        Get all available offices from  the table in database
        """
        query="""
        SELECT * FROM offices
        """
        offices = database.select_from_database(query)
        offices_lst = []
        for office in offices:
            # convert party tuple to a dictionary - which is easily jsonified
            offices_lst.append(Office.to_json(office))
        return offices_lst


    @classmethod
    def get_office_by_id(cls, id):
        """
        Get a specific  office  from the table in database by its id
        "/parties/<int:id>"
        """
        query=""" SELECT * FROM offices WHERE office_id='{}'
        """.format(id)
        office = database.select_from_database(query)
        try:
            office = Office.to_json(office[0])
        except:

            print("No office found")
        return office

    @classmethod
    def delete_office(cls, id):
        """
        Remove a specific  office  from the table in database.
        """
        office = Office.get_office_by_id(id)
        if office:
            query="""
            DELETE FROM offices WHERE id='{}' 
            """.format(id)
            try:
                conn, cursor = database.connect_db()
                conn.execute(query)
                conn.commit()
                conn.close()
            except psycopg2.Error as error:
                print (error)
    


    @classmethod
    def to_json(self, office_row):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "office_id": office_row[0],
            "office_type": office_row[1],
            "office_name": office_row[2]
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
        """
        Add a new user to the database
        only i there is no  user with similar info
        """

        query = """
        INSERT INTO users(firstname, lastname, username, email, password, phoneNumber, passport_url) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.first_name, self.last_name, self.username, self.email, self.password, self.phone_number, self.passport_url )
        

        database.insert_to_db(query)

    @classmethod
    def get_user_by_phone_number(cls, phone_number):
        """
        Get a user by their phone number
        """

        query = """
        SELECT * FROM users WHERE users.phoneNumber='{}'
        """.format(phone_number)

        user = database.select_from_database(query)
        return user

    @classmethod
    def  get_user_by_username(cls, username):
        """
        Get a user by their username
        """

        query = """
        SELECT * FROM users WHERE username='{}'
        """.format(username)

        user = database.select_from_database(query)
        return user

    @classmethod
    def  get_user_by_email(cls, email):
        """
        Get a user by their email
        Returns the user and all their info if email is found
        """

        query = """
        SELECT email FROM users WHERE users.email='{}'
        """.format(email)

        email = database.select_from_database(query)
        return email

    @staticmethod
    def get_user_by_password(password):

        query = """
        SELECT password FROM users WHERE users.password='{}'
        """.format(password)

        password = database.select_from_database(query)
        return password
    
    def to_json(self, user_row):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "id": user_row[0],
            "first_name": user_row[1],
            "last_name": user_row[2],
            "username":  user_row[3],
            "email": user_row[4],
            "phone_number": user_row[6],
            "passport_url": user_row[7]
        }

class Candidates:
    def __init__(self, id, candidate_name, office_id, party_id):
        self.candidate_name = candidate_name
        self.office_id = office_id
        self.party_id = party_id

    def create_candidate():
        """
        Add a candidate to the database in the candidates tables
        only if it does not exist
        """
        query = """
        INSERT INTO users(candidate_name, office_id, party_id) VALUES(
            '{}', '{}', '{}'
        )""".format(self.candidate_name, self.office_id, self.party_id)
        database.insert_to_db(query)


    def does_candidate_exist(candidate_id, office_id):
        """
        Check if a candidate exists in the  database in the candidates tables
        Goes through the entire candidates table and returns a candidate if they find a match and returns
        "candidate not found" if the candidate does not exist
        """
        query = """
        SELECT candidate_name, office_id FROM candiddates WHERE candidates.candidate_name AND candidates.office_id VALUES(
            '{}', '{}'
        )""".format(self.candidate_name, self.office_id)

        candidate= database.select_from_db(query)
        return candidate


    def add_candidate_to_database():
        """
        Adds a new candidate to the database by appending their infointo 
        the candidates table
        """
        query = """
        INSERT INTO candidates(candidate_name, office_id) VALUES(
            '{}', '{}'
        )""".format(self.candidate_name, self.office_id)
        database.insert_to_db(query)

    


    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
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

        query = """
        INSERT INTO votes(createdOn, createBy, candidateVoteFor, officeVotedFor) VALUES(
            '{}', '{}', '{}', '{}'
        )""".format(self.createdOn, self.createBy, self.candidateVoteFor, self.officeVotedFor)
        

        database.insert_to_db(query)


    def user_vote():
        query="""
        SELECT createdBy, officeVotedFor FROM votes WHERE votes.createdBy='{}'  AND votes.officeVotedFor='{}'""".format(createdBy,officeVotedFor)
    def to_json(self):
        """
        convert from object to dictionary
        for easy rendering as json response
        """
        return {
            "id": user_row[0],
            "createdOn": user_row[1],
            "createBy": user_row[2],
            "candidateVoteFor":  user_row[3],
            "officeVotedFor": user_row[4]

        }