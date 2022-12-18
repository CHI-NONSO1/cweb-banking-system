# Generated by Django 4.1.1 on 2022-09-28 11:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(blank=True, default=0, null=True)),
                ('fullname', models.CharField(max_length=200)),
                ('phoneno', models.CharField(max_length=200)),
                ('transaction_ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('bank_adminid', models.CharField(max_length=200)),
                ('teller_adminid', models.CharField(max_length=200)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_adminid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('phoneno', models.CharField(max_length=15)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('balance', models.IntegerField(blank=True, default=0, null=True)),
                ('charges', models.IntegerField(blank=True, default=0, null=True)),
                ('job_title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawal', models.IntegerField(default=0)),
                ('charges', models.IntegerField(default=0)),
                ('fullname', models.CharField(max_length=200)),
                ('phoneno', models.CharField(max_length=200)),
                ('transaction_ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('customer_accountid', models.CharField(max_length=200)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_accountid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('phoneno', models.CharField(max_length=15)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('balance', models.IntegerField(blank=True, default=0, null=True)),
                ('imageKYC', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FrontDeskAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fron_deask_adminid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('phoneno', models.CharField(max_length=15)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('job_title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TellerAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teller_adminid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('phoneno', models.CharField(max_length=15)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('balance', models.IntegerField(blank=True, default=0, null=True)),
                ('job_title', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transactins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.IntegerField(blank=True, default=0, null=True)),
                ('withdrawal', models.IntegerField(blank=True, default=0, null=True)),
                ('charges', models.IntegerField(blank=True, default=0, null=True)),
                ('fullname', models.CharField(max_length=200)),
                ('phoneno', models.CharField(max_length=200)),
                ('transaction_ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('customer_accountid', models.CharField(max_length=200)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
    ]
