import http.client
import pprint
import json

async def get_ghl_contacts():
    # Step 1: Establish a connection to the server
    conn = http.client.HTTPSConnection("services.leadconnectorhq.com")

    # Step 2: Set up the headers for authorization and content type
    headers = {
        'Authorization': "Bearer pit-48e307a2-761c-4bae-af44-442750b8904b",
        'Version': "2021-07-28",
        'Accept': "application/json"
    }

    # Step 3: Make a GET request to fetch all contacts data
    conn.request("GET", "/contacts/?locationId=4rKuULHASyQ99nwdL1XH", headers=headers)

    # Step 4: Get the response from the server
    res = conn.getresponse()
    data = res.read()

    # Step 5: Decode the JSON response to a string
    data_str = data.decode("utf-8")

    # Step 6: Load the string into a Python dictionary
    data_dict = json.loads(data_str)

    # Step 7: Access the contacts list from the dictionary
    contacts = data_dict["contacts"]

    # Step 8: Pretty print the contacts data for better visualization
    print("All contacts:")
    # pprint.pprint(contacts)

    # Step 9: Access and pretty print a single contact example by index
    print("\nSingle contact at index 0:")
    single_contact = contacts[0]
    # pprint.pprint(single_contact)

    # Step 10: Access specific fields from a single contact
    # print("\nAccess specific fields of a single contact:")
    # print(f"ID: {single_contact['id']}")
    # print(f"Name: {single_contact['contactName']}")
    # print(f"Email: {single_contact['email']}")
    # print(f"Phone: {single_contact['phone']}")

    return contacts
