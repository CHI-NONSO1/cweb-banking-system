from django.utils import timezone
import os
from django.conf import settings
from django.shortcuts import redirect, render
from bank_admin.models import CustomerAdmin, FrontDeskAdmin, Transactions
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
import uuid
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date, datetime
from PIL import Image
import PIL


def Dashboard(request, token):
    target_page = 'front_desk/front-desk.html'
    access_token = FrontDeskAdmin.objects.filter(refresh_token=token).values()
    desk_token = access_token[0]['refresh_token']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    phoneno = access_token[0]['phoneno']
    email = access_token[0]['email']
    image = access_token[0]['image']

    context = {
        'token': desk_token,
        'firstname': firstname,
        'lastname': lastname,
        'phoneno': phoneno,
        'image': image,
        'email': email
    }
    return render(request, target_page, context)


def FrontDeskRegister(request):
    if request.method == 'POST':
        passwd = request.POST.get('password')
        front_desk = FrontDeskAdmin()
        front_desk.firstname = request.POST.get('firstname')
        front_desk.lastname = request.POST.get('lastname')
        front_desk.email = request.POST.get('email')
        front_desk.phoneno = request.POST.get('phoneno')
        front_desk.password = make_password(passwd)
        front_desk.image = request.FILES.get('file')

        front_desk.save()

        return redirect('http://127.0.0.1:8000/front-desk-login')
    else:
        return render(request, 'front_desk/front-desk-register.html', {'error_message': "Your password didn't match", })


def FrontDeskLogin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = FrontDeskAdmin.objects.get(email=email)
        us = FrontDeskAdmin.objects.values('password')
        lo = list(us)[0]['password']
        usercheck = check_password(password, lo)
        if user and usercheck:
            tokenid = uuid.uuid4()
            FrontDeskAdmin.objects.filter(email=email).update(
                refresh_token=tokenid)
            access = FrontDeskAdmin.objects.filter(email=email).values()
            access_token = access[0]['refresh_token']

            return HttpResponseRedirect(reverse('bank_admin:front-desk', args=[str(access_token)],))

            # return redirect('http://127.0.0.1:8000/front-desk', {'data': tokenid})

        else:
            return render(request, 'front_desk/front-desk-login.html', {'error_message': "You Email or Password is incorrect! ."})
    else:

        return render(request, 'front_desk/front-desk-login.html', {})


def FrontDeskLogout(request, token):
    FrontDeskAdmin.objects.filter(refresh_token=token).update(
        refresh_token='None')

    return redirect('http://127.0.0.1:8000/front-desk-login', {})


def FrontDeskAccountDetail(request, token):
    target_page = 'front_desk/account-detail.html'
    access_token = FrontDeskAdmin.objects.filter(refresh_token=token).values()
    desk_token = access_token[0]['refresh_token']
    email = access_token[0]['email']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']

    context = {
        'token': desk_token,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
    }
    return render(request, target_page, context)


def UpdateAccount(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        token = request.POST.get('token')
        city = request.POST.get('city')
        address = request.POST.get('address')
        job_title = request.POST.get('jobtitle')
        # new_img = request.FILES.get('file')
        # old_img = FrontDeskAdmin.objects.filter(email=email).values()
        # old_img_name = old_img[0]['image']
        # ty = old_img_name.strip('images/')
        # path = r"C:/Users/Agwara/cweb_banking_system/Scripts/cweb_banking_system/media/images/"
        # img = Image.open(path+ty+'eg')
        # img.save(path + new_img)

        FrontDeskAdmin.objects.filter(email=email).update(
            city=city,
            address=address,
            job_title=job_title,
            # image='images/' + str(new_img),
            updatedAt=timezone.now())

        return HttpResponseRedirect(reverse('bank_admin:update-status', args=[str(token)],))

    else:
        return render(request, 'front_desk/account-detail.html', {'error_message': "Something went wrong!", })


def UpdateAccountStatus(request, token):
    target_page = 'front_desk/update-status.html'
    access_token = FrontDeskAdmin.objects.filter(refresh_token=token).values()
    desk_token = access_token[0]['refresh_token']
    email = access_token[0]['email']
    city = access_token[0]['city']
    address = access_token[0]['address']
    job_title = access_token[0]['job_title']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']

    context = {
        'data': 'Update Successful!',
        'token': desk_token,
        'email': email,
        'city': city,
        'address': address,
        'job_title': job_title,
        'firstname': firstname,
        'lastname': lastname,

    }
    return render(request, target_page, context)


def PageCustomerAccount(request, token):
    target_page = 'front_desk/customer-number.html'
    context = {
        'token': token,
    }
    return render(request, target_page, context)


def CustomerDetailPage(request):
    if request.method == 'POST':
        phoneno = request.POST.get('phoneno')
        token = request.POST.get('token')
        target_page = 'front_desk/customer-detail-page.html'
        customer_info = CustomerAdmin.objects.filter(phoneno=phoneno).values()
        firstname = customer_info[0]['firstname']
        email = customer_info[0]['email']
        city = customer_info[0]['city']
        address = customer_info[0]['address']
        lastname = customer_info[0]['lastname']
        phoneno = customer_info[0]['phoneno']
        imageKYC = customer_info[0]['imageKYC']
        image = customer_info[0]['image']
        customerid = customer_info[0]['customer_accountid']
        createdAt = customer_info[0]['createdAt']
        balance = customer_info[0]['balance']
        updatedAt = customer_info[0]['updatedAt']
        frontDesk = FrontDeskAdmin.objects.filter(
            refresh_token=token).values()
        FrontDeskFirstName = frontDesk[0]['firstname']
        FrontDeskLastName = frontDesk[0]['lastname']
        context = {

            'token': token,
            'email': email,
            'city': city,
            'address': address,
            'firstname': firstname,
            'phoneno': phoneno,
            'lastname': lastname,
            'imageKYC': imageKYC,
            'image': image,
            'data': 'Active',
            'createdAt': createdAt,
            'balance': balance,
            'updatedAt': updatedAt,
            'customerid': customerid,
            'FrontDeskFirstName': FrontDeskFirstName,
            'FrontDeskLastName': FrontDeskLastName,

        }
        return render(request, target_page, context)


def AllCustomerPage(request, token):
    target_page = 'front_desk/allcustomer-page.html'
    data = CustomerAdmin.objects.all().values()
    frontDesk = FrontDeskAdmin.objects.filter(
        refresh_token=token).values()
    FrontDeskFirstName = frontDesk[0]['firstname']
    FrontDeskLastName = frontDesk[0]['lastname']
    return render(
        request,
        target_page,
        {
            'data': data,
            'token': token,
            'FrontDeskFirstName': FrontDeskFirstName,
            'FrontDeskLastName': FrontDeskLastName,
        })


def CustomerAction(request, customer_accountid, token):
    target_page = 'front_desk/customer-detail-page.html'

    customer_info = CustomerAdmin.objects.filter(
        customer_accountid=customer_accountid).values()
    firstname = customer_info[0]['firstname']
    email = customer_info[0]['email']
    city = customer_info[0]['city']
    address = customer_info[0]['address']
    lastname = customer_info[0]['lastname']
    phoneno = customer_info[0]['phoneno']
    imageKYC = customer_info[0]['imageKYC']
    image = customer_info[0]['image']
    customerid = customer_info[0]['customer_accountid']
    createdAt = customer_info[0]['createdAt']
    balance = customer_info[0]['balance']

    context = {

        'token': token,
        'email': email,
        'city': city,
        'address': address,
        'firstname': firstname,
        'phoneno': phoneno,
        'lastname': lastname,
        'imageKYC': imageKYC,
        'image': image,
        'data': 'Active',
        'createdAt': createdAt,
        'balance': balance,
        'customerid': customerid,


    }
    return render(request, target_page, context)


def BlockCustomer(request, customerid, token):
    customer_info = CustomerAdmin.objects.filter(
        customer_accountid=customerid)
    action = customer_info.delete()
    #action = 'I commented this portion out for now '
    if action:
        target_page = 'front_desk/allcustomer-page.html'
        data = CustomerAdmin.objects.all().values()
        return render(request, target_page, {'data': data, 'token': token})


def CustomerUpdateForm(request, customerid, token):
    target_page = 'front_desk/customer-update-form.html'
    frontDesk = FrontDeskAdmin.objects.filter(
        refresh_token=token).values()
    FrontDeskFirstName = frontDesk[0]['firstname']
    FrontDeskLastName = frontDesk[0]['lastname']
    context = {
        'token': token,
        'customerid': customerid,
        'firstname': FrontDeskFirstName,
        'lastname': FrontDeskLastName,
    }
    return render(request, target_page, context)


def UpdateCustomerAccount(request):
    target_page = 'front_desk/customer-detail-page.html'
    if request.method == 'POST':
        token = request.POST.get('token')
        city = request.POST.get('city')
        address = request.POST.get('address')
        customer_accountid = request.POST.get('customerid')
        # new_img = request.FILES.get('file')
        # old_img = FrontDeskAdmin.objects.filter(email=email).values()
        # old_img_name = old_img[0]['image']
        # ty = old_img_name.strip('images/')
        # path = r"C:/Users/Agwara/cweb_banking_system/Scripts/cweb_banking_system/media/images/"
        # img = Image.open(path+ty+'eg')
        # img.save(path + new_img)

        customer_update = CustomerAdmin.objects.filter(customer_accountid=customer_accountid).update(
            city=city,
            address=address,

            # image='images/' + str(new_img),
            updatedAt=timezone.now())
        if customer_update:

            customer_info = CustomerAdmin.objects.filter(
                customer_accountid=customer_accountid).values()
            firstname = customer_info[0]['firstname']
            email = customer_info[0]['email']
            city = customer_info[0]['city']
            address = customer_info[0]['address']
            lastname = customer_info[0]['lastname']
            phoneno = customer_info[0]['phoneno']
            imageKYC = customer_info[0]['imageKYC']
            image = customer_info[0]['image']
            customerid = customer_info[0]['customer_accountid']
            createdAt = customer_info[0]['createdAt']
            balance = customer_info[0]['balance']
            updatedAt = customer_info[0]['updatedAt']

            context = {
                'status': 'update Successful',
                'token': token,
                'email': email,
                'city': city,
                'address': address,
                'firstname': firstname,
                'phoneno': phoneno,
                'lastname': lastname,
                'imageKYC': imageKYC,
                'image': image,
                'data': 'Active',
                'createdAt': createdAt,
                'balance': balance,
                'customerid': customerid,
                'updatedAt': updatedAt,

            }

        return render(request, target_page, context)


def CustomerAccountHistoryForm(request, token):
    target_page = 'front_desk/customer-transaction-history-form.html'
    frontDesk = FrontDeskAdmin.objects.filter(
        refresh_token=token).values()
    FrontDeskFirstName = frontDesk[0]['firstname']
    FrontDeskLastName = frontDesk[0]['lastname']
    context = {
        'token': token,
        'firstname': FrontDeskFirstName,
        'lastname': FrontDeskLastName,
    }
    return render(request, target_page, context)


# def CustomerAccountHistory(request):
#     if request.method == 'POST':
#         phoneno = request.POST.get('phoneno')
#         token = request.POST.get('token')
#         target_page = 'front_desk/customer-transaction-history.html'
#         transactions = Transactions.objects.filter(phoneno=phoneno).values()
#         fullname = transactions[0]['fullname']
#         withdrawal = transactions[0]['withdrawal']
#         deposit = transactions[0]['deposit']
#         charges = transactions[0]['charges']
#         transaction_ref = transactions[0]['transaction_ref']
#         phoneno = transactions[0]['teller_adminid']
#         customer_accountid = transactions[0]['customer_accountid']
#         createdAt = transactions[0]['createdAt']

#         context = {

#             'token': token,
#             'withdrawal': withdrawal,
#             'transaction_ref': transaction_ref,
#             'fullname': fullname,
#             'phoneno': phoneno,
#             'deposit': deposit,
#             'createdAt': createdAt,
#             'charges': charges,
#             'customer_accountid': customer_accountid,

#         }
#         return render(request, target_page, context)

def CustomerAccountHistory(request):
    if request.method == 'POST':
        phoneno = request.POST.get('phoneno')
        token = request.POST.get('token')
        target_page = 'front_desk/customer-transaction-history.html'
        data = Transactions.objects.filter(phoneno=phoneno).values()
        frontDesk = FrontDeskAdmin.objects.filter(
            refresh_token=token).values()
        FrontDeskFirstName = frontDesk[0]['firstname']
        FrontDeskLastName = frontDesk[0]['lastname']

    return render(
        request,
        target_page,
        {
            'data': data,
            'token': token,
            'firstname': FrontDeskFirstName,
            'lastname': FrontDeskLastName,
        })
