from api.v2.models import database
import psycopg2

class Party:
    def __init__(self, name, hqaddress, logo_url):
        self.name = name
        self.hqaddress = hqaddress
        self.logo_url = logo_url
    
    def create_party(self):
        query = """
        INSERT INTO parties(party_name, hqAddress, logo_url) VALUES(
            '{}', '{}', '{}')
        """.format(self.name, self.hqaddress, self.logo_url)
        database.insert_to_db(query)

    @classmethod
    def get_party_by_name(cls, name):
        query = """
        SELECT * FROM parties WHERE party_name='{}'
        """.format(name)
        user = database.select_from_database(query)
        return user

    @classmethod
    def get_all_parties(cls):
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
        query=""" SELECT * FROM parties WHERE party_id='{}'
        """.format(id)
        party = database.select_from_database(query)
        return Party.to_json(party[0])


    # """
    # add patch endpoint to update a party by id
    #     dont forget!!!!!
    # """

    @classmethod
    def delete_party(cls, id):
        """
        update a political party
        """
        party = Party.get_party_by_id(id)

        if party:
            query="""
            DELETE FROM parties WHERE id='{}' 
            """.format(id)
            try:
                conn, cursor = database.connect_db()
                conn.execute(query)
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
        query = """
        INSERT INTO offices(office_type, office_name) VALUES(
            '{}', '{}')
        """.format(self.office_type, self.name)
        database.insert_to_db(query)

    @classmethod
    def get_office_by_name(cls, name):
        query = """
        SELECT * FROM offices WHERE office_name='{}'
        """.format(name)
        user = database.select_from_database(query)
        return user


    @classmethod
    def get_all_offices(cls):
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
        query=""" SELECT * FROM offices WHERE office_id='{}'
        """.format(id)
        office = database.select_from_database(query)
        return Office.to_json(office[0])

    @classmethod
    def delete_office(cls, id):
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

        query = """
        INSERT INTO users(firstname, lastname, username, email, password, phoneNumber, passport_url) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.first_name, self.last_name, self.username, self.email, self.password, self.phone_number, self.passport_url )
        

        database.insert_to_db(query)

    @classmethod
    def get_user_by_phone_number(cls, phone_number):

        query = """
        SELECT * FROM users WHERE users.phoneNumber='{}'
        """.format(phone_number)

        user = database.select_from_database(query)
        return user

    @classmethod
    def  get_user_by_username(cls, username):

        query = """
        SELECT * FROM users WHERE username='{}'
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
