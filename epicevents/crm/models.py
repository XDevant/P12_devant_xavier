from django.db import models, transaction
from django.conf import settings


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, null=True)
    sales_contact = models.ForeignKey(
                                      to=settings.AUTH_USER_MODEL,
                                      on_delete=models.PROTECT,
                                      related_name='client_contact'
                                      )

    def __str__(self):
        return str(self.id)


class Contract(models.Model):
    client = models.ForeignKey(
                               to=Client,
                               on_delete=models.CASCADE,
                               related_name='contractor'
                               )
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='contract_contact'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return str(self.id)


class Status(models.Model):
    contract = models.ForeignKey(
                               to=Contract,
                               on_delete=models.CASCADE,
                               related_name='contract_status'
                               )

    def __str__(self):
        return str(self.contract.status)


class Event(models.Model):
    client = models.ForeignKey(
                               to=Client,
                               on_delete=models.CASCADE,
                               related_name='event_client'
                               )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=None, null=True)
    support_contact = models.ForeignKey(
                                        to=settings.AUTH_USER_MODEL,
                                        on_delete=models.PROTECT,
                                        related_name='event_support'
                                        )
    event_status = models.OneToOneField(
                                        to=Status,
                                        on_delete=models.CASCADE,
                                        )
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=500, null=True)

    @transaction.atomic()
    def delete(self, using=None, keep_parents=False):
        status = self.event_status
        contract = status.contract
        contract.status = False
        contract.save()
        status.delete()
        super().delete()

    def __str__(self):
        return str(self.id)
