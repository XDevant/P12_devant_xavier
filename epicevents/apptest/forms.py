from datetime import date

client_form = {
                "first_name":  "third",
                "last_name":  "client",
                "email":  "third@client.co",
                "phone":  "01",
                "mobile":  "08",
                "company_name":  "World"
              }

expected_client = {}

contract_form = {
                "client_id":  1,
                "amount":  15,
                "payment_due":  "2022-08-17"
                }

expected_contract = {}

event_form = {
        "contact_email": "bi@bi.co",
        "status":  3,
        "attendees":  15,
        "event_date":  "2022-08-17",
        "notes": "bla"
             }

expected_event = {'id': 3,
                  'client_id': '1',
                  'status': 'True',
                  'contact_email': 'Bi Bi couriel:bi@bi.co',
                  'attendees': 15,
                  'event_date': '2022-08-17Z',
                  'notes': 'bla',
                  'date_created': date.today()
                  }
