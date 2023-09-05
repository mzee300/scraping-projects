from hubspot import HubSpot
from hubspot.crm import companies
from hubspot.crm import contacts
import json

api_client = HubSpot(access_token='pat-na1-539289b1-8eb3-4342-8923-e9dee35402ca')

# all_contacts = api_client.crm.contacts.get_all()
# print(all_contacts)
def create_company(company_inputs):
    try:
        simple_public_object_input_companies = companies.SimplePublicObjectInput(
            properties=company_inputs
        )
        api_response = api_client.crm.companies.basic_api.create(
            simple_public_object_input=simple_public_object_input_companies
        )
        return api_response.id

    except companies.exceptions.ApiException as e:

        print("Exception when creating contact: %s\n" % e)
        try:
            data = json.loads(e.body)
            company_id = data.get('message', '').split('.')[1].split(' ')[1]
            print(company_id)
            return company_id
        except:
            return ''
        return ''


def create_contact(contact_input):
    try:
        simple_public_object_input = contacts.SimplePublicObjectInput(
            properties=contact_input)
        api_response = api_client.crm.contacts.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )
        return api_response
    except contacts.exceptions.ApiException as e:
        print("Exception when creating contact: %s\n" % e)
        return ''















