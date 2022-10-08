"""This file contains 3 sets of data needed for the tests of each 3 models.
The _form is used to create a new item.
The expected is the expected response to this creation
The expected_1 items are supposed to be the pk=1 of each model. This last one
is heavily dependent on the copy_Epic-Events DB.
"""
from datetime import datetime


client_form = {
                "first_name":  "third",
                "last_name":  "client",
                "email":  "third@client.co",
                "phone":  "01",
                "mobile":  "08",
                "company_name":  "World"
              }

expected_client = {'id': 5,
                   'first_name': 'third',
                   'last_name': 'client',
                   'email': 'third@client.co',
                   'phone': '01', 'mobile': '08',
                   'company_name': 'World',
                   'date_created': datetime.now(),
                   'contact': 'De De couriel:de@de.co'
                   }

expected_client_1 = {'id': 1,
                     'first_name': 'First',
                     'last_name': 'Client',
                     'email': 'first@client.co',
                     'phone': '01',
                     'mobile': '06',
                     'company_name': 'World',
                     'date_created': '2022-09-29',
                     'contact': 'De De couriel:de@de.co'
                     }

contract_form = {
    "client_id":  1,
    "amount":  15,
    "payment_due":  "2050-10-10T10:00:00+01:00"
}

expected_contract = {
    "id": 9,
    "contact": "de@de.co",
    "client_id": 1,
    "date_created": datetime.now(),
    "status": False,
    "amount":  15.,
    "payment_due": "2050-10-10T10:00:00+01:00"
}

expected_contract_1 = {
    "id": 1,
    "client_id": 1,
    "status": True,
    "amount": 1000.,
    "payment_due": "2040-10-10T10:00:00+01:00",
    "contact": "de@de.co",
    "date_created": "2022-10-05T23:00:00Z"
}

event_form = {
        "contact_email": "bi@bi.co",
        "status":  2,
        "attendees":  15,
        "event_date":  "2030-10-10T10:00:00+01:00",
        "notes": "bla"
}

expected_event = {
    'id': 5,
    'client_id': '1',
    'status': 'True',
    'contact_email': 'Bi Bi couriel:bi@bi.co',
    'attendees': 15,
    'event_date': "2030-10-10T10:00:00+01:00",
    'notes': 'bla',
    'date_created': datetime.now()
}

expected_event_1 = {
    'id': 1,
    'client_id': '1',
    'status': 'True',
    'contact_email': 'Bi Bi couriel:bi@bi.co',
    'attendees': 10,
    'event_date': "2026-10-10T10:00:00+01:00",
    'notes': 'test event 1',
    'date_created': '2022-09-29'
}
