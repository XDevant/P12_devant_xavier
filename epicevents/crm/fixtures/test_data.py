from datetime import timedelta, timezone, datetime


test_clients = [
  {
      "first_name":  "First",
      "last_name":  "Client",
      "email":  "first@client.co",
      "phone":  "01",
      "mobile":  "06",
      "company_name":  "World",
      "sales_contact":  0
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
]
test_contracts = [
  {
      "client":  0,
      "amount":  10,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
  {
      "client":  1,
      "amount":  11,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
{
      "client":  0,
      "amount":  100,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
  {
      "client":  1,
      "amount":  110,
      "payment_due": datetime.now(timezone.utc) + timedelta(days=28),
  },
]
test_events = [
  {
      "support_contact":  0,
      "event_status":  0,
      "attendees":  10,
      "event_date":  datetime.now(timezone.utc) + timedelta(days=40),
      "notes": "test event 1"
  },
  {
      "support_contact":  1,
      "event_status":  1,
      "attendees":  20,
      "event_date":  datetime.now(timezone.utc) + timedelta(days=20),
      "notes": "test event 2"
  },
]
