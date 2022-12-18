
from django.shortcuts import render
from bank_admin.models import AdminTransfer, BankAdmin, TellerAdmin


def FundAdminAccountForm(request, token):
    target_page = 'bank_admin/add-fund-form.html'
    admin_token = BankAdmin.objects.filter(refresh_token=token).values()
    data = admin_token[0]['bank_adminid']
    firstname = admin_token[0]['firstname']
    lastname = admin_token[0]['lastname']
    balance = admin_token[0]['balance']
    charges = admin_token[0]['charges']
    context = {
        'data': data,
        'token': token,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,

    }
    if admin_token == None:
        return render(request, 'bank_admin/bank-admin.html', {})
    else:
        return render(request, target_page, context)


def FundAdminAccount(request, token):
    target_page = 'bank_admin/bank-admin.html'

    amount = request.POST.get('amount')

    admin_token = BankAdmin.objects.filter(refresh_token=token).values()
    balance = admin_token[0]['balance']
    addedAmount = int(balance) + int(amount)
    BankAdmin.objects.filter(
        refresh_token=token).update(balance=addedAmount)

    access_token = BankAdmin.objects.filter(refresh_token=token).values()
    data = access_token[0]['bank_adminid']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']
    charges = access_token[0]['charges']
    context = {
        'data': data,
        'token': token,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,

    }

    return render(request, target_page, context)


def GetTeller(request, token):
    target_page = 'admin_transfer/teller-account.html'
    admin_token = BankAdmin.objects.filter(refresh_token=token).values()
    data = admin_token[0]['bank_adminid']
    firstname = admin_token[0]['firstname']
    lastname = admin_token[0]['lastname']
    balance = admin_token[0]['balance']
    charges = admin_token[0]['charges']
    context = {
        'data': data,
        'token': token,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'charges': charges,

    }
    if admin_token == None:
        return render(request, 'bank_admin/bank-admin.html', {})
    else:
        return render(request, target_page, context)


def GetTellerNumber(request):
    target_page = 'admin_transfer/transfer-teller.html'
    phoneno = request.POST.get('number')
    adminid = request.POST.get('adminid')
    bal = TellerAdmin.objects.filter(phoneno=phoneno).values()
    bankadminid = BankAdmin.objects.filter(bank_adminid=adminid).values()
    id = bankadminid[0]['bank_adminid']
    token = bankadminid[0]['refresh_token']
    firstname = bankadminid[0]['firstname']
    lastname = bankadminid[0]['lastname']
    balance = bankadminid[0]['balance']
    charges = bankadminid[0]['charges']
    cv = bal[0]['balance']
    num = bal[0]['phoneno']
    if adminid == None:
        return render(request, 'bank_admin/bank-admin.html', {})
    elif cv == None or cv == []:
        context = {
            'bal': 0,
            'num': num,
            'id': id,
            'token': token,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        }

    else:
        context = {
            'bal': cv,
            'num': num,
            'id': id,
            'token': token,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        }
    return render(request, target_page, context)


def TransferToTeller(request):
    target_page = 'admin_transfer/transfer-successful.html'

    phoneno = request.POST.get('number')
    adminid = request.POST.get('adminid')
    amount = request.POST.get('amount')

    adminbal = BankAdmin.objects.filter(bank_adminid=adminid).values()
    adminbala = adminbal[0]['balance']
    fullname = adminbal[0]['firstname']
    firstname = adminbal[0]['firstname']
    lastname = adminbal[0]['lastname']
    balance = adminbal[0]['balance']
    charges = adminbal[0]['charges']
    admin_return_token = adminbal[0]['refresh_token']
    if adminid == None:
        return render(request, 'bank_admin/bank-admin.html', {})

    elif adminbala == None or int(adminbala) == 0 or int(adminbala) < int(amount):
        context = {'data': 'Not enough balance'}
        return context
    adminnewbal = int(adminbala) - int(amount)
    admin_transfer = BankAdmin.objects.filter(
        bank_adminid=adminid).update(balance=adminnewbal)
    if admin_transfer:
        bal = TellerAdmin.objects.filter(phoneno=phoneno).values()
        teller_prev_bal = bal[0]['balance']
        teller_adminid = bal[0]['teller_adminid']
        tellerName = bal[0]['firstname']

        if teller_prev_bal == None:
            teller_prev_bal = 0
        else:
            teller_new_bal = int(teller_prev_bal) + int(amount)
            TellerAdmin.objects.filter(
                phoneno=phoneno).update(balance=teller_new_bal)

        transfer = AdminTransfer()
        transfer.balance = amount
        transfer.fullname = fullname
        transfer.bank_adminid = adminid
        transfer.teller_adminid = teller_adminid
        transfer.phoneno = phoneno
        transfer.save()

        context = {
            'data': 'Transfer Successful',
            'token': admin_return_token,
            'amount': amount,
            'name': tellerName,
            'adminId': adminid,
            'tellerNum': phoneno,
            'firstname': firstname,
            'lastname': lastname,
            'balance': balance,
            'charges': charges,
        }
    return render(request, target_page, context)
