# Imports

import unittest
import json
import os

from api.v2 import create_app
from api.v2.models.database import drop_tables, initiate_database
from api.v2.utils.helpers import decode_token

class Partiesv2TestCase(unittest.TestCase):
    #set up tests
    def setUp(self):
        """
        create testing app
        set up testing variables
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        initiate_database(os.getenv("DATABASE_TEST_URL"))

        # sample data
        self.user_signup = {
            "first_name":"uhf",
            "last_name":"dzvfd",
            "username":"xvxdfv",
            "email":"your@them.com",
            "phone_number":"9996857",
            "passport_url":"dsfdd",
            "role": "candidate",
            "password":"Aaaaaaaaa",
            "confirm_password":"Aaaaaaaaa" 
        }

        self.user_signup_1 = {
            "first_name":"uhf",
            "last_name":"dzvfd",
            "username":"username",
            "email":"your@email.com",
            "phone_number":"0955443",
            "passport_url":"dsfdd",
            "role": "candidate",
            "password":"Aaaaaaaaa",
            "confirm_password":"Aaaaaaaaa" 
        }

        self.user_login = {
            "username":"username",
            "password":"Aaaaaaaaa"
        }

        self.token = ""

        self.party = {
            "name": "Party 1",
            "hqaddress": "address 1",
            "logo_url": "http://logo.url"
        }
        self.party_2 = {
            "name": "Party 22",
            "hqaddress": "address 22",
            "logo_url": "http://logo22.url"
        }
        self.party_empty_fields = {
            "name": "Party 2",
            "hqaddress": "",
            "logo_url": ""
        }

        self.party_invalid_payload_keys = {
            "name": "Party 2",
            "hqaddress": "address 2",
            "logo_address": "http://logo2.url"# invalid key - should be logo_url
        }

        # Office variables
        self.office = {
            "office_name": "office 1",
            "office_type": "head"
        }
        self.office_empty_fields = {
            "office_name": "Office 2",
            "office_type": ""
        }
        self.office_invalid_payload_keys = {
            "office_name": "2 office" ,#invalid key - should be logo_url
            "office_type": "head" 
        }
        
    def login(self):
        """
        Login a fake user to acquire token"
        """
        sign_up_response = self.client.post("api/v2/auth/sign-up", data = json.dumps(self.user_signup_1), content_type='application/json')
        response = self.client.post("api/v2/auth/signin", data=json.dumps(self.user_login), content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        result_2 = json.loads(sign_up_response.data.decode('utf-8'))

        self.token = result['token']
        return self.token

    def test_create_party_successfully(self):
        # data payload - data sent by the user
        self.token = self.login()
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party), headers={'token_Bearer':self.token}, content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Party created successfully.")
        self.assertEqual(response.status_code, 201)

    #validation tests
    def test_create_party_rejects_empty_fields(self):
        self.token = self.login()
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party_empty_fields), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "hqaddress is required")
        self.assertEqual(response.status_code, 400)

    def test_create_party_rejects_incorrect_payload_keys(self):
        self.token = self.login()
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party_invalid_payload_keys), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"],"Use appropriate keys." )
        self.assertTrue(response.status_code == 400)

    def test_create_party_rejects_duplicate_party_name(self):
        self.token = self.login()
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)
        # # attempt to create the same party again
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "A party with a similar name exists")
        self.assertEqual(response.status_code, 400)

    def test_fetch_all_parties_successfully(self):
        self.token = self.login()
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)
        # fetch
        response = self.client.get("/api/v2/parties", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data.decode('utf-8'))["message"], "Parties fetched successfully.")
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_party_successfully(self):
        self.token = self.login()
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party), headers={'token_Bearer':self.token}, content_type='application/json')
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/v2/parties/1", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party fetched successfully.")
        self.assertEqual(response.status_code, 200)

    def test_fetch_no_parties_found(self):
        self.token = self.login()
        response = self.client.get("/api/v2/parties", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "There are no parties.")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_specififc_party(self):
        # create sample party
        self.token = self.login()
        
        response = self.client.post("/api/v2/parties", data=json.dumps(self.party), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)

        response = self.client.delete("/api/v2/parties/1", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party deleted successfully.")
        
    def test_create_office_successfully(self):
        # data payload - data sent by the user
        self.token = self.login()
        response = self.client.post("/api/v2/offices", data=json.dumps(self.office), headers={'token_Bearer':self.token}, content_type='application/json')
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
    
    def test_create_office_rejects_empty_fields(self):
        self.token = self.login()
        response = self.client.post("/api/v2/offices", data=json.dumps(self.office_empty_fields), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)["error"], "office_type is required")
        

    def test_create_office_rejects_incorrect_payload_keys(self):
        self.token = self.login()
        response = self.client.post("/api/v2/offices", data=json.dumps(self.party_invalid_payload_keys), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"],"Use appropriate keys." )
        self.assertTrue(response.status_code == 400)

    
    def test_create_party_rejects_duplicate_office_name(self):
        self.token = self.login()
        response = self.client.post("/api/v2/offices", data=json.dumps(self.office), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
        # # attempt to create the same party again
        response = self.client.post("/api/v2/offices", data=json.dumps(self.office), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "An office with a similar name exists")
        self.assertEqual(response.status_code, 400)

    def test_fetch_all_offices_successfully(self):
        self.token = self.login()
        response = self.client.post("/api/v2/offices", data=json.dumps(self.office), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
        # fetch
        response = self.client.get("/api/v2/offices", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Offices fetched successfully.")
        self.assertEqual(response.status_code, 200)


    def test_fetch_single_office_successfully(self):
        self.token = self.login()
        response = self.client.post("/api/v2/offices", data=json.dumps(self.office), headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/v2/offices/1", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office fetched successfully.")
        self.assertEqual(response.status_code, 200)

    def test_fetch_no_office_found(self):
        self.token = self.login()
        response = self.client.get("/api/v2/offices/1", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "Office not found.")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_specififc_office(self):
        self.token = self.login()
        response = self.client.get("/api/v2/offices", headers={'token_Bearer':self.token}, content_type="application/json")
        self.assertNotIn(json.loads(response.data)["message"], "Office deleted sucessfully.")

    def tearDown(self):
        """
        restore variables to default as defined in setup
        destroy app context
        """
        self.app_context.pop()
        self.client = None
        drop_tables(os.getenv("DATABASE_TEST_URL"))

        

if __name__ == '__main__':
    unittest.main()
