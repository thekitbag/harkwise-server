import hubspot, os
from pprint import pprint
from hubspot.crm.contacts import SimplePublicObjectInputForCreate, ApiException

FLASK_ENV = os.environ.get('FLASK_ENV')
client = hubspot.Client.create(access_token=os.environ.get("HUBSPOT_TOKEN"))

def add_contact(firstName, lastName, phoneNumber, email, businessName):
    properties = {
        "email": email,
        "firstname": firstName,
        "lastname": lastName,
        "phone": phoneNumber,
        "company": businessName
    }
    if FLASK_ENV == 'prod' :
        simple_public_object_input_for_create = SimplePublicObjectInputForCreate(associations=[], properties=properties)
        try:
            api_response = client.crm.contacts.basic_api.create(simple_public_object_input_for_create=simple_public_object_input_for_create)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling basic_api->create: %s\n" % e)
    else:
        print('Hubspot API Call would happen here')