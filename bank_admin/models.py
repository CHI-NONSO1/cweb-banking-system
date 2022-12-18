from django.db import models
import uuid

# Create your models here.


class BankAdmin(models.Model):
    bank_adminid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(max_length=50)
    image = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    phoneno = models.CharField(max_length=15)
    city = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    address = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    charges = models.IntegerField(default=0, blank=True, null=True)
    job_title = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class FrontDeskAdmin(models.Model):
    fron_deask_adminid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(max_length=50)
    image = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    phoneno = models.CharField(max_length=15)
    city = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    address = models.CharField(
        max_length=255, default=None, blank=True, null=True)

    job_title = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class CustomerAdmin(models.Model):
    customer_accountid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(max_length=50)
    image = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    phoneno = models.CharField(max_length=15)
    city = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    address = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    imageKYC = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    # def __str__(self):
    #     return self.email + '' + self.firstname + ' ' + self.lastname + '' + self.balance + ' ' + self.refresh_token + ' ' + self.phoneno


class TellerAdmin(models.Model):
    teller_adminid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=500)
    refresh_token = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(max_length=50)
    image = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    phoneno = models.CharField(max_length=15)
    city = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    address = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    job_title = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    # def __str__(self):
    #     return int(self.balance)
        # return int(self.email + '' + self.firstname + ' ' + self.lastname + '' + str(self.balance) + ' ' + str(self.#refresh_token) + ' ' + str(self.phoneno) + ' ' + str(self.teller_adminid))


class Transactions(models.Model):
    deposit = models.IntegerField(default=0, blank=True, null=True)
    withdrawal = models.IntegerField(default=0, blank=True, null=True)
    charges = models.IntegerField(default=0, blank=True, null=True)
    fullname = models.CharField(max_length=200)
    phoneno = models.CharField(max_length=200)
    transaction_ref = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    teller_adminid = models.CharField(max_length=200)
    customer_accountid = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)


class Charges(models.Model):
    withdrawal = models.IntegerField(default=0)
    charges = models.IntegerField(default=0)
    fullname = models.CharField(max_length=200)
    phoneno = models.CharField(max_length=200)
    transaction_ref = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    customer_accountid = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)


class AdminTransfer(models.Model):
    balance = models.IntegerField(default=0, blank=True, null=True)
    fullname = models.CharField(max_length=200)
    phoneno = models.CharField(max_length=200)
    transaction_ref = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    bank_adminid = models.CharField(max_length=200)
    teller_adminid = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(default=None, null=True)
