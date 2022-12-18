from django.test import TestCase

# Create your tests here.
from django.test.utils import setup_test_environment
from django.test import Client
from bank_admin.models import CustomerAdmin
# setup_test_environment()


# client = Client()
# resp = client.get('/')
# resp.status_code
# resp.content

class CheckCustomerPhonenoField(TestCase):
    def checkAccountNumber(self):
       # phoneno = ''
        register = CustomerAdmin.objects.all()  # (phoneno=phoneno)
        # self.assertIs(register)
        greeting = 'Hello World!'
        self.assertContains(greeting, 'Hello')
