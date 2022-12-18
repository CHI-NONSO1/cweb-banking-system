from django.utils import timezone
from django.shortcuts import redirect, render
from bank_admin.models import AdminTransfer, BankAdmin, TellerAdmin, Transactions
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
import uuid
from django.http import HttpResponseRedirect
from django.urls import reverse


def bankAdmin(request, admin):
    target_page = 'bank_admin/bank-admin.html'
    token = BankAdmin.objects.filter(refresh_token=admin).values()
    teller_token = token[0]['refresh_token']
    firstname = token[0]['firstname']
    lastname = token[0]['lastname']
    phoneno = token[0]['phoneno']
    email = token[0]['email']
    image = token[0]['image']
    balance = token[0]['balance']
    charges = token[0]['charges']
    context = {
        'token': teller_token,
        'firstname': firstname,
        'lastname': lastname,
        'phoneno': phoneno,
        'image': image,
        'balance': balance,
        'email': email,
        'charges': charges
    }
    return render(request, target_page, context)


def bankAdminRegister(request):
    if request.method == 'POST':
        passwd = request.POST.get('password')
        admin = BankAdmin()
        admin.firstname = request.POST.get('firstname')
        admin.lastname = request.POST.get('lastname')
        admin.email = request.POST.get('email')
        admin.phoneno = request.POST.get('phoneno')
        admin.password = make_password(passwd)
        admin.image = request.FILES.get('file')
        admin.balance = request.POST.get('balance')

        admin.save()

        return redirect('http://127.0.0.1:8000/login-admin')
    else:
        return render(request, 'bank_admin/bank-admin-register.html', {'error_message': "Your password didn't match", })


def LoginAdmin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = BankAdmin.objects.get(email=email)
        us = BankAdmin.objects.values('password')
        lo = list(us)[0]['password']
        usercheck = check_password(password, lo)
        if user and usercheck:
            tokenid = uuid.uuid4()
            BankAdmin.objects.filter(email=email).update(
                refresh_token=tokenid)

            access = BankAdmin.objects.filter(email=email).values()
            access_token = access[0]['refresh_token']

            return HttpResponseRedirect(reverse('bank_admin:bank-admin', args=[str(access_token)],))

        else:
            return render(request, 'bank_admin/bank-admin-login.html', {'error_message': "You ."})
    else:

        return render(request, 'bank_admin/bank-admin-login.html', {})


def AdminLogout(request, token):
    BankAdmin.objects.filter(refresh_token=token).update(
        refresh_token='None')

    return redirect('http://127.0.0.1:8000/login-admin', {})


def BankAdminAccountDetail(request, token):
    target_page = 'bank_admin/bank-admin-account-detail.html'
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    admin_token = access_token[0]['refresh_token']
    email = access_token[0]['email']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']

    context = {
        'token': admin_token,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,
    }
    return render(request, target_page, context)


def BankAdminUpdateAccount(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        token = request.POST.get('token')
        city = request.POST.get('city')
        address = request.POST.get('address')
        job_title = request.POST.get('jobtitle')
        # new_img = request.FILES.get('file')
        # old_img = BankAdmin.objects.filter(email=email).values()
        # old_img_name = old_img[0]['image']
        # ty = old_img_name.strip('images/')
        # path = r"C:/Users/Agwara/cweb_banking_system/Scripts/cweb_banking_system/media/images/"
        # img = Image.open(path+ty+'eg')
        # img.save(path + new_img)

        BankAdmin.objects.filter(email=email).update(
            city=city,
            address=address,
            job_title=job_title,
            # image='images/' + str(new_img),
            updatedAt=timezone.now())

        return HttpResponseRedirect(reverse('bank_admin:bank-admin-update-status', args=[str(token)],))

    else:
        return render(request, 'bank_admin/bank-admin-account-detail.html', {'error_message': "Something went wrong!", })


def BankAdminUpdateAccountStatus(request, token):
    target_page = 'bank_admin/bank-admin-update-status.html'
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    admin_token = access_token[0]['refresh_token']
    email = access_token[0]['email']
    city = access_token[0]['city']
    address = access_token[0]['address']
    job_title = access_token[0]['job_title']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']

    context = {
        'data': 'Update Successful!',
        'token': admin_token,
        'email': email,
        'city': city,
        'address': address,
        'job_title': job_title,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,

    }
    return render(request, target_page, context)


def PageTellerAccount(request, token):
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    target_page = 'bank_admin/teller-number.html'
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']
    context = {
        'token': token,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,
    }
    return render(request, target_page, context)


def TellerDetailPage(request):
    if request.method == 'POST':
        phoneno = request.POST.get('phoneno')
        token = request.POST.get('token')
        target_page = 'bank_admin/teller-detail-page.html'
        teller_info = TellerAdmin.objects.filter(phoneno=phoneno).values()
        firstname = teller_info[0]['firstname']
        email = teller_info[0]['email']
        city = teller_info[0]['city']
        address = teller_info[0]['address']
        lastname = teller_info[0]['lastname']
        phoneno = teller_info[0]['phoneno']
        image = teller_info[0]['image']
        tellerid = teller_info[0]['teller_adminid']
        createdAt = teller_info[0]['createdAt']
        balance = teller_info[0]['balance']
        updatedAt = teller_info[0]['updatedAt']
        access_token = BankAdmin.objects.filter(refresh_token=token).values()

        adminfirstname = access_token[0]['firstname']
        adminlastname = access_token[0]['lastname']
        adminbalance = access_token[0]['balance']
        charges = access_token[0]['charges']
        context = {

            'token': token,
            'email': email,
            'city': city,
            'address': address,
            'firstname': firstname,
            'phoneno': phoneno,
            'lastname': lastname,
            'image': image,
            'data': 'Active',
            'createdAt': createdAt,
            'balance': balance,
            'updatedAt': updatedAt,
            'tellerid': tellerid,
            'adminfirstname': adminfirstname,
            'adminlastname': adminlastname,
            'adminbalance': adminbalance,
            'charges': charges,

        }
        return render(request, target_page, context)


def AllTellerPage(request, token):
    target_page = 'bank_admin/all-teller-page.html'
    data = TellerAdmin.objects.all().values()
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']
    return render(
        request,
        target_page,
        {
            'data': data,
            'token': token,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        })


def TellerAction(request, teller_adminid, token):
    target_page = 'bank_admin/teller-detail-page.html'

    teller_info = TellerAdmin.objects.filter(
        teller_adminid=teller_adminid).values()
    firstname = teller_info[0]['firstname']
    email = teller_info[0]['email']
    city = teller_info[0]['city']
    address = teller_info[0]['address']
    lastname = teller_info[0]['lastname']
    phoneno = teller_info[0]['phoneno']
    image = teller_info[0]['image']
    tellerid = teller_info[0]['teller_adminid']
    createdAt = teller_info[0]['createdAt']
    balance = teller_info[0]['balance']

    context = {

        'token': token,
        'email': email,
        'city': city,
        'address': address,
        'firstname': firstname,
        'phoneno': phoneno,
        'lastname': lastname,
        'image': image,
        'data': 'Active',
        'createdAt': createdAt,
        'balance': balance,
        'tellerid': tellerid,

    }
    return render(request, target_page, context)


def BlockTeller(request, tellerid, token):
    teller_info = TellerAdmin.objects.filter(
        teller_adminid=tellerid)
    # action = teller_info.delete()
    action = ' I disabled delete'
    if action:
        target_page = 'bank_admin/all-teller-page.html'
        data = TellerAdmin.objects.all().values()
        return render(request, target_page, {'data': data, 'token': token})


def TellerAccountHistoryForm(request, token):
    target_page = 'bank_admin/teller-transaction-history-form.html'
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']
    context = {
        'token': token,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,
    }
    return render(request, target_page, context)


def TellerAccountHistory(request):
    if request.method == 'POST':
        phoneno = request.POST.get('phoneno')
        token = request.POST.get('token')
        target_page = 'bank_admin/teller-transaction-history.html'
        data = Transactions.objects.filter(phoneno=phoneno).values()
        access_token = BankAdmin.objects.filter(refresh_token=token).values()
        firstname = access_token[0]['firstname']
        lastname = access_token[0]['lastname']
        balance = access_token[0]['balance']
        charges = access_token[0]['charges']

    return render(
        request,
        target_page,
        {
            'data': data,
            'token': token,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        })


def TransactionHistory(request, token):
    target_page = 'bank_admin/transaction-history.html'
    data = Transactions.objects.all().values()
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']

    return render(
        request,
        target_page,
        {
            'data': data,
            'token': token,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        })


def DeleteTransaction(request, transaction_ref, token):
    transaction_info = Transactions.objects.filter(
        transaction_ref=transaction_ref)
    action = transaction_info.delete()
    #action = ' I disabled delete'
    if action:
        target_page = 'bank_admin/transaction-history.html'
        data = Transactions.objects.all().values()
        return render(request, target_page, {'data': data, 'token': token})


def SingleTransactionHistory(request, transaction_ref, token):
    target_page = 'bank_admin/single-transaction-history-page.html'
    data = Transactions.objects.filter(
        transaction_ref=transaction_ref).values()
    fullname = data[0]['fullname']
    phoneno = data[0]['phoneno']
    deposit = data[0]['deposit']
    charges = data[0]['charges']
    withdrawal = data[0]['withdrawal']
    T_ref = data[0]['transaction_ref']
    tellerid = data[0]['teller_adminid']
    customerid = data[0]['customer_accountid']
    createdAt = data[0]['createdAt']

    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    adminchargeinflow = access_token[0]['charges']

    return render(
        request,
        target_page,
        {

            'token': token,
            'fullname': fullname,
            'phoneno': phoneno,
            'deposit': deposit,
            'charges': charges,
            'withdrawal': withdrawal,
            'T_ref': T_ref,
            'customerid': customerid,
            'tellerid': tellerid,
            'createdAt': createdAt,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'adminchargeinflow': adminchargeinflow,
        })


def SingleAdminTransferHistory(request, transaction_ref, token):
    target_page = 'bank_admin/single-admin-transfer-history-page.html'
    data = AdminTransfer.objects.filter(
        transaction_ref=transaction_ref).values()
    fullname = data[0]['fullname']
    phoneno = data[0]['phoneno']
    transferAmount = data[0]['balance']
    T_ref = data[0]['transaction_ref']
    tellerid = data[0]['teller_adminid']
    adminid = data[0]['bank_adminid']
    createdAt = data[0]['createdAt']

    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    adminchargeinflow = access_token[0]['charges']

    return render(
        request,
        target_page,
        {

            'token': token,
            'fullname': fullname,
            'phoneno': phoneno,
            'transferAmount': transferAmount,
            'T_ref': T_ref,
            'adminid': adminid,
            'tellerid': tellerid,
            'createdAt': createdAt,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'adminchargeinflow': adminchargeinflow,
        })


def AdminTransactionHistory(request, token):
    target_page = 'bank_admin/bank-admin-transaction-history.html'
    data = AdminTransfer.objects.all().values()
    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']
    return render(
        request,
        target_page,
        {
            'data': data,
            'token': token,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        })


def DeleteTransfer(request, transaction_ref, token):
    transfer_info = AdminTransfer.objects.filter(
        transaction_ref=transaction_ref)
    action = transfer_info.delete()
    #action = ' I disabled delete'
    if action:
        target_page = 'bank_admin/bank-admin-transaction-history.html'
        data = AdminTransfer.objects.all().values()
        return render(request, target_page, {'data': data, 'token': token})
