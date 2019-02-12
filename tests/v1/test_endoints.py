# Imports

import unittest
import json

from api.v1 import create_app
from api.v1.models import PARTIES, OFFICES


class PartiesV1TestCase(unittest.TestCase):
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

        # sample data
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
            "name": "office 1",
            "office_type": "head"
        }
        self.office_empty_fields = {
            "name": "Office 2",
            "office_type": ""
        }
        self.office_invalid_payload_keys = {
            "name": "2 office" ,#invalid key - should be logo_url
            "office_type": "head" 
        }

    def test_create_party_successfully(self):
        # data payload - data sent by the user
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party), content_type='application/json')
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)

    # #validation tests
    def test_create_party_rejects_empty_fields(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party_empty_fields), content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "All fields are required.")
        self.assertEqual(response.status_code, 400)

    def test_create_party_rejects_incorrect_payload_keys(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party_invalid_payload_keys), content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"],"Use appropriate keys." )
        self.assertTrue(response.status_code == 400)

    def test_create_party_rejects_duplicate_party_name(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party), content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)
        # # attempt to create the same party again
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party), content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "A party with a similar name exists")
        self.assertEqual(response.status_code, 409)

    def test_fetch_all_parties_successfully(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party), content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)
        # fetch
        response = self.client.get("/api/v1/parties", content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Parties fetched successfully.")
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_party_successfully(self):
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party), content_type='application/json')
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)
        # 
        response = self.client.get("/api/v1/parties/1", content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party fetched successfully.")
        self.assertEqual(response.status_code, 200)

    def test_fetch_no_parties_found(self):
        response = self.client.get("/api/v1/parties", content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "There are no parties.")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_specififc_party(self):
        # create sample party
        sample_party = {"name": "Party x", "hqaddress": "address x", "logo_url": "http://logo_x.url"}
        response = self.client.post("/api/v1/parties", data=json.dumps(self.party), content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party created successfully.")
        self.assertEqual(response.status_code, 201)

        response = self.client.delete("/api/v1/parties/1", content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Party deleted sucessfully.")
        
    def test_create_office_successfully(self):
        # data payload - data sent by the user
        response = self.client.post("/api/v1/offices", data=json.dumps(self.office), content_type='application/json')
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
    
    def test_create_office_rejects_empty_fields(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(self.office_empty_fields), content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "All fields are required.")
        self.assertEqual(response.status_code, 400)

    def test_create_office_rejects_incorrect_payload_keys(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(self.party_invalid_payload_keys), content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"],"Use appropriate keys." )
        self.assertTrue(response.status_code == 400)

    
    def test_create_party_rejects_duplicate_office_name(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(self.office), content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
        # # attempt to create the same party again
        response = self.client.post("/api/v1/offices", data=json.dumps(self.office), content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "An office with a similar name exists")
        self.assertEqual(response.status_code, 409)

    def test_fetch_all_offices_successfully(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(self.office), content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
        # fetch
        response = self.client.get("/api/v1/offices", content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Offices fetched successfully.")
        self.assertEqual(response.status_code, 200)


    def test_fetch_single_office_successfully(self):
        response = self.client.post("/api/v1/offices", data=json.dumps(self.office), content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office created successfully.")
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/v1/offices/1", content_type="application/json")
        self.assertEqual(json.loads(response.data)["message"], "Office fetched successfully.")
        self.assertEqual(response.status_code, 200)

    def test_fetch_no_office_found(self):
        
        response = self.client.get("/api/v1/offices/1", content_type="application/json")
        self.assertEqual(json.loads(response.data)["error"], "Office not found.")
        self.assertEqual(response.status_code, 404)
    
    def test_delete_specififc_office(self):
        response = self.client.get("/api/v1/offices", content_type="application/json")
        self.assertNotIn(json.loads(response.data)["message"], "Office deleted sucessfully.")

    def tearDown(self):
        """
        restore variables to default as defined in setup
        destroy app context
        """
        self.app_context.pop()
        self.client = None
        PARTIES.clear()
        OFFICES.clear()
    

if __name__ == '__main__':
    unittest.main()
