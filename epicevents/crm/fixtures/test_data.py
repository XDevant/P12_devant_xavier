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
      "payment_due": datetime(2040, 10, 10, timezone.utc),
  },
  {
      "client":  1,
      "amount":  2000,
      "payment_due": datetime(2041, 10, 10, timezone.utc),
  },
{
      "client":  0,
      "amount":  10000,
      "payment_due": datetime(2042, 10, 10, timezone.utc),
  },
  {
      "client":  1,
      "amount":  20000,
      "payment_due": datetime(2043, 10, 10, timezone.utc),
  },
{
      "client":  2,
      "amount":  100000,
      "payment_due": datetime(2050, 10, 10, timezone.utc),
  },
  {
      "client":  3,
      "amount":  200000,
      "payment_due": datetime(2051, 10, 10, timezone.utc),
  },
{
      "client":  2,
      "amount":  30000,
      "payment_due": datetime(2052, 10, 10, timezone.utc),
  },
  {
      "client":  3,
      "amount":  40000,
      "payment_due": datetime(2053, 10, 10, timezone.utc),
  },
]
test_events = [
  {
      "support_contact":  0,
      "event_status":  0,
      "attendees":  10,
      "event_date":  datetime(2050, 10, 10, timezone.utc),
      "notes": "test event 1"
  },
  {
      "support_contact":  1,
      "event_status":  1,
      "attendees":  20,
      "event_date": datetime(2050, 10, 10, timezone.utc),
      "notes": "test event 2"
  },
{
      "support_contact":  0,
      "event_status":  2,
      "attendees":  1000,
      "event_date":  datetime(2030, 10, 10, timezone.utc),
      "notes": "test event 3"
  },
  {
      "support_contact":  1,
      "event_status":  3,
      "attendees":  2000,
      "event_date": datetime(2030, 10, 10, timezone.utc),
      "notes": "test event 4"
  },
]
