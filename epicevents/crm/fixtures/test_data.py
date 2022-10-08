from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings


test_clients = [
  {
      "first_name":     "First",
      "last_name":      "Client",
      "email":          "first@client.co",
      "phone":          "01",
      "mobile":         "06",
      "company_name":   "World",
      "sales_contact":  0,
  },
  {
      "first_name":  "Second",
      "last_name":  "Butnotlast",
      "email":  "second@butnotlast.co",
      "phone":  "02",
      "mobile":  "07",
      "company_name":  "Mega",
      "sales_contact":  1
  },
  {
      "first_name":  "Third",
      "last_name":  "Brave",
      "email":  "third@brave.co",
      "phone":  "03",
      "mobile":  "08",
      "company_name":  "BlackPebble",
      "sales_contact":  0
  },
  {
      "first_name":  "Fourth",
      "last_name":  "Sork",
      "email":  "fourth@sork.co",
      "phone":  "04",
      "mobile":  "09",
      "company_name":  "Ewing Oil",
      "sales_contact":  1
  },
]
test_contracts = [
  {
      "client":  0,
      "amount":  1000,
      "payment_due": "2040-10-10T10:00:00+01:00"
  },
  {
      "client":  1,
      "amount":  2000,
      "payment_due": "2041-10-10T10:00:00+01:00"
  },
  {
      "client":  0,
      "amount":  10000,
      "payment_due": "2042-10-10T10:00:00+01:00"
  },
  {
      "client":  1,
      "amount":  20000,
      "payment_due": "2043-10-10T10:00:00+01:00"
  },
  {
      "client":  2,
      "amount":  100000,
      "payment_due": "2030-10-10T10:00:00+01:00"
  },
  {
      "client":  3,
      "amount":  200000,
      "payment_due": "2031-10-10T10:00:00+01:00"
  },
  {
      "client":  2,
      "amount":  30000,
      "payment_due": "2032-10-10T10:00:00+01:00"
  },
  {
      "client":  3,
      "amount":  40000,
      "payment_due": "2033-10-10T10:00:00+01:00"
  },
]
test_events = [
  {
      "support_contact":  0,
      "event_status":  0,
      "attendees":  10,
      "event_date":  "2026-10-10T10:00:00+01:00",
      "notes": "test event 1"
  },
  {
      "support_contact":  1,
      "event_status":  1,
      "attendees":  20,
      "event_date": "2027-10-10T10:00:00+01:00",
      "notes": "test event 2"
  },
  {
      "support_contact":  0,
      "event_status":  2,
      "attendees":  1000,
      "event_date":  "2028-10-10T10:00:00+01:00",
      "notes": "test event 3"
  },
  {
      "support_contact":  1,
      "event_status":  3,
      "attendees":  2000,
      "event_date": "2029-10-10T10:00:00+01:00",
      "notes": "test event 4"
  },
]
