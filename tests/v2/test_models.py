# #imports
# import unittest

# from api.v2 import create_app
# from api.v2.models.database import drop_tables, initiate_database
# from api.v2.models.models import Party, Office



# class PartiesModelsv2TestCase(unittest.TestCase):
#     def setUp(self):
#         """
#         create testing app
#         set up testing variables
#         """
#         self.party = Party(name="Party 1", hqaddress="addr 1", logo_url="http://logo.png")    
#         self.office = Office(name="Office 1", office_type="head")
#         self.app = create_app("testing")
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         initiate_database(os.getenv("DATABASE_TEST_URL"))

#         # sample data
#         self.user_signup = {
#             "first_name":"uhf",
#             "last_name":"dzvfd",
#             "username":"xvxdfv",
#             "email":"your@them.com",
#             "phone_number":"9996857",
#             "passport_url":"dsfdd",
#             "password":"Aaaaaaaaa",
#             "confirm_password":"Aaaaaaaaa" 
#         }

#         self.user_signup_1 = {
#             "first_name":"uhf",
#             "last_name":"dzvfd",
#             "username":"username",
#             "email":"your@email.com",
#             "phone_number":"0987655443",
#             "passport_url":"dsfdd",
#             "password":"Aaaaaaaaa",
#             "confirm_password":"Aaaaaaaaa" 
#         }

#         self.user_login = {
#             "username":"username",
#             "password":"Aaaaaaaaa"
#         }

#         self.token = ""

#         self.party = {
#             "name": "Party 1",
#             "hqaddress": "address 1",
#             "logo_url": "http://logo.url"
#         }
#         self.party_2 = {
#             "name": "Party 22",
#             "hqaddress": "address 22",
#             "logo_url": "http://logo22.url"
#         }
#         self.party_empty_fields = {
#             "name": "Party 2",
#             "hqaddress": "",
#             "logo_url": ""
#         }

#         self.party_invalid_payload_keys = {
#             "name": "Party 2",
#             "hqaddress": "address 2",
#             "logo_address": "http://logo2.url"# invalid key - should be logo_url
#         }

#         # Office variables
#         self.office = {
#             "office_name": "office 1",
#             "office_type": "head"
#         }
#         self.office_empty_fields = {
#             "office_name": "Office 2",
#             "office_type": ""
#         }
#         self.office_invalid_payload_keys = {
#             "office_name": "2 office" ,#invalid key - should be logo_url
#             "office_type": "head" 
#         }

#     def tearDown(self):
#         self.app_context.pop()
#         self.client = None
#         # initiate_database(os.getenv("DATABASE_TEST_URL"))
#         drop_tables()

#         # PARTIES.clear()
#         # OFFICES.clear()
    
#     def test_create_party(self):
#         self.party.create_party()
#         # self.assertEqual(len(PARTIES), 1)

#     def test_get_party_by_name(self):
#         # create party
#         self.party.create_party()
#         # self.assertEqual(len(PARTIES), 1)
#         # get by name
#         self.assertEqual(Party.get_party_by_name(self.party.name).name, "Party 1")
    
#     def test_get_all_parties(self):
#         self.party.create_party()
#         self.assertEqual(len(PARTIES), 1)
#         self.assertEqual(len(Party.get_all_parties()), 1)

#     def test_get_party_by_id(self):
#          # create party
#         self.party.create_party()
#         self.assertEqual(len(PARTIES), 1)
#         # get by name
#         self.assertEqual(Party.get_party_by_id(self.party.id).name, "Party 1")

#     def test_create_office(self):
#         self.office.create_office()
#         self.assertEqual(len(OFFICES), 1)

#     def test_get_office_by_name(self):
#         # create office
#         self.office.create_office()
#         self.assertEqual(len(OFFICES), 1)
#         # get by name
#         self.assertEqual(Office.get_office_by_name(self.office.name).name, "Office 1")
   
#     def test_get_all_offices(self):
#         self.office.create_office()
#         self.assertEqual(len(OFFICES), 1)

#         # self.assertEqual(Office.get_all_offices(self.office), "Office 1")

#     def test_get_office_by_id(self):
#          # create party
#         self.office.create_office()
#         self.assertEqual(len(OFFICES), 1)
#         # get by name
#         self.assertEqual(Office.get_office_by_id(self.office.id).name , "Office 1")

#     def test_delete_office(self):
#         self.office.create_office()
#         self.assertEqual(len(OFFICES), 1)
#         # delete office
#         Office.delete_office(self.office.id)
#         self.assertEqual(len(OFFICES), 0)


    
#     def tearDown(self):
#         pass
#         # PARTIES.clear()
#         # OFFICES.clear()


    
# if __name__ == '__main__':
#     unittest.main()
