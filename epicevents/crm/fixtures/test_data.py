from datetime import timedelta, timezone, datetime


test_clients = [
  {
      "first_name":  "first",
      "last_name":  "client",
      "email":  "first@client.co",
      "phone":  "01",
      "mobile":  "06",
      "company_name":  "World",
      "sales_contact":  0
  },
  {
      "first_name":  "second",
      "last_name":  "client",
      "email":  "second@client.co",
      "phone":  "02",
      "mobile":  "07",
      "company_name":  "Mega",
      "sales_contact":  1
  },
]
test_contracts = [
  {
      "sales_contact": 0,
      "client":  0,
      "status":  True,
      "amount":  10,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
  {
      "sales_contact": 1,
      "client":  1,
      "status":  True,
      "amount":  10,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
{
      "sales_contact": 0,
      "client":  0,
      "status":  False,
      "amount":  100,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
  {
      "sales_contact": 1,
      "client":  1,
      "status":  False,
      "amount":  100,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
]
test_events = [
  {
      "support_contact":  0,
      "client":  0,
      "event_status":  0,
      "attendees":  10,
      "event_date":  datetime.now(timezone.utc) + timedelta(days=40),
      "notes": "test event 1"
  },
  {
      "support_contact":  1,
      "client":  1,
      "event_status":  1,
      "attendees":  20,
      "event_date":  datetime.now(timezone.utc) + timedelta(days=20),
      "notes": "test event 2"
  },
]
