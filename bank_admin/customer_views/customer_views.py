from atexit import register
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from bank_admin.models import CustomerAdmin, Transactions
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
# Create your views here.
import uuid


def Dashboard(request, customer):
    target_page = 'customer/my-bank.html'
    token = CustomerAdmin.objects.filter(refresh_token=customer).values()
    user_token = token[0]['refresh_token']
    firstname = token[0]['firstname']
    lastname = token[0]['lastname']
    phoneno = token[0]['phoneno']
    email = token[0]['email']
    customerid = token[0]['customer_accountid']
    image = token[0]['image']
    balance = token[0]['balance']
    if balance == None:
        balance = 0
    else:
        balance = balance
    context = {
        'token': user_token,
        'firstname': firstname,
        'lastname': lastname,
        'phoneno': phoneno,
        'image': image,
        'balance': balance,
        'email': email,
        'customerid': customerid,

    }

    return render(request, target_page, context)


def CustomerRegister(request):
    if request.method == 'POST':
        passwd = request.POST.get('password')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = make_password(passwd)
        phoneno = request.POST.get('phoneno')
        obj, customer = CustomerAdmin.objects.get_or_create(
            phoneno=phoneno,
            email=email,

            defaults={
                'email': email,
                'phoneno': phoneno,
                'firstname': firstname,
                'lastname': lastname,
                'password': password,
            }
        )
        if customer == False:
            return render(request, 'customer/customer-register.html', {'error_message': obj, })
        else:
            return redirect('http://127.0.0.1:8000/customer-login', {'error_message': obj, })

    else:
        return render(request, 'customer/customer-register.html', {'welcome_message': "Create An Account to Experience the new Era of Digital Payment!", })


def CustomerLogin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomerAdmin.objects.get(email=email)
        passaccess = CustomerAdmin.objects.filter(email=email).values()
        passwd = passaccess[0]['password']
        usercheck = check_password(password, passwd)
        if user and usercheck:
            tokenid = uuid.uuid4()
            CustomerAdmin.objects.filter(email=email).update(
                refresh_token=tokenid)
            access = CustomerAdmin.objects.filter(email=email).values()
            access_token = access[0]['refresh_token']

            return HttpResponseRedirect(reverse('bank_admin:dashboard', args=[str(access_token)],))

        else:
            return render(request, 'customer/customer-login.html', {'error_message': "Your Email or Password is incorrect ."})
    else:

        return render(request, 'customer/customer-login.html', {})


def CustomerLogout(request, token):
    loggedout = CustomerAdmin.objects.filter(refresh_token=token).update(
        refresh_token='None')
    if loggedout:
        return redirect('http://127.0.0.1:8000/customer-login', {})


def CustomerTransactionHistory(request, customerid):
    target_page = 'customer/transaction-history.html'
    data = Transactions.objects.filter(customer_accountid=customerid).values()
    token = CustomerAdmin.objects.filter(
        customer_accountid=customerid).values()
    user_token = token[0]['refresh_token']
    firstname = token[0]['firstname']
    lastname = token[0]['lastname']
    phoneno = token[0]['phoneno']
    balance = token[0]['balance']

    return render(
        request, target_page,
        {
            'data': data,
            'firstname': firstname,
            'lastname': lastname,
            'phoneno': phoneno,
            'balance': balance,
            'customer': user_token,

        })


def CustomerTransactionHistoryDetail(request, transaction_ref, token):
    target_page = 'customer/transaction-history-detail-page.html'
    data = Transactions.objects.filter(
        transaction_ref=transaction_ref).values()
    deposit = data[0]['deposit']
    withdrawal = data[0]['withdrawal']
    charge = data[0]['charges']
    customername = data[0]['fullname']
    customernum = data[0]['phoneno']
    T_ref = data[0]['transaction_ref']
    customerid = data[0]['customer_accountid']
    tellerid = data[0]['teller_adminid']
    createdAt = data[0]['createdAt']

    token = CustomerAdmin.objects.filter(
        refresh_token=token).values()
    user_token = token[0]['refresh_token']
    firstname = token[0]['firstname']
    lastname = token[0]['lastname']
    phoneno = token[0]['phoneno']
    balance = token[0]['balance']

    return render(
        request, target_page,
        {
            'deposit': deposit,
            'withdrawal': withdrawal,
            'charge': charge,
            'customername': customername,
            'T_ref': T_ref,
            'customerid': customerid,
            'tellerid': tellerid,
            'createdAt': createdAt,
            'customernum': customernum,
            'firstname': firstname,
            'lastname': lastname,
            'phoneno': phoneno,
            'balance': balance,
            'token': user_token,

        })
