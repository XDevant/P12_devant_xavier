from django.db import models
from django.conf import settings


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    sales_contact = models.ForeignKey(
                                      to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='client_contact'
                                      )


class Contract(models.Model):
    sales_contact = models.ForeignKey(
                                      to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='contract_contact'
                                      )
    client = models.ForeignKey(
                               to=Client,
                               on_delete=models.CASCADE,
                               related_name='contractor'
                               )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()


class Event(models.Model):
    client = models.ForeignKey(
                               to=Client,
                               on_delete=models.CASCADE,
                               related_name='event_client'
                               )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    support_contact = models.ForeignKey(
                                        to=settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE,
                                        related_name='event_support'
                                        )
    event_status = models.CharField(max_length=20)
    attendees = models.IntegerField
    event_date = models.DateTimeField()
    notes = models.TextField()
