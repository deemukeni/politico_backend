#imports
import unittest

from api.v1 import create_app
from api.v1.models import Party, Office, PARTIES, OFFICES


class PartiesModelsV1TestCase(unittest.TestCase):
    def setUp(self):
        """
        create testing app
        set up testing variables
        """
        self.party = Party(name="Party 1", hqaddress="addr 1", logo_url="http://logo.png")    
        self.office = Office(name="Office 1", office_type="head")

    def tearDown(self):
        PARTIES.clear()
        OFFICES.clear()
    
    def test_create_party(self):
        self.party.create_party()
        self.assertEqual(len(PARTIES), 1)

    def test_get_party_by_name(self):
        # create party
        self.party.create_party()
        self.assertEqual(len(PARTIES), 1)
        # get by name
        self.assertEqual(Party.get_party_by_name(self.party.name).name, "Party 1")
    
    def test_get_all_parties(self):
        self.party.create_party()
        self.assertEqual(len(PARTIES), 1)
        self.assertEqual(len(Party.get_all_parties()), 1)

    def test_get_party_by_id(self):
         # create party
        self.party.create_party()
        self.assertEqual(len(PARTIES), 1)
        # get by name
        self.assertEqual(Party.get_party_by_id(self.party.id).name, "Party 1")

    def test_create_office(self):
        self.office.create_office()
        self.assertEqual(len(OFFICES), 1)

    def test_get_office_by_name(self):
        # create office
        self.office.create_office()
        self.assertEqual(len(OFFICES), 1)
        # get by name
        self.assertEqual(Office.get_office_by_name(self.office.name).name, "Office 1")
   
    def test_get_all_offices(self):
        self.office.create_office()
        self.assertEqual(len(OFFICES), 1)

        # self.assertEqual(Office.get_all_offices(self.office), "Office 1")

    def test_get_office_by_id(self):
         # create party
        self.office.create_office()
        self.assertEqual(len(OFFICES), 1)
        # get by name
        self.assertEqual(Office.get_office_by_id(self.office.id).name , "Office 1")

    def test_delete_office(self):
        self.office.create_office()
        self.assertEqual(len(OFFICES), 1)
        # delete office
        Office.delete_office(self.office.id)
        self.assertEqual(len(OFFICES), 0)


    
    def tearDown(self):
        PARTIES.clear()
        OFFICES.clear()


    

if __name__ == '__main__':
    unittest.main()
