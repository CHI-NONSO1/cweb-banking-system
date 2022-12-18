# Generated by Django 4.1.1 on 2022-10-01 13:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bank_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.IntegerField(blank=True, default=0, null=True)),
                ('withdrawal', models.IntegerField(blank=True, default=0, null=True)),
                ('charges', models.IntegerField(blank=True, default=0, null=True)),
                ('fullname', models.CharField(max_length=200)),
                ('phoneno', models.CharField(max_length=200)),
                ('transaction_ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('teller_adminid', models.CharField(max_length=200)),
                ('customer_accountid', models.CharField(max_length=200)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Transactins',
        ),
    ]