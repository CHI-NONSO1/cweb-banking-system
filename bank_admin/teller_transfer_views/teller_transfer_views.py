
from django.shortcuts import render
from bank_admin.models import BankAdmin, Charges, Transactions, TellerAdmin, CustomerAdmin


def GetCustomer(request, token):
    target_page = 'teller_transfer/customer-account.html'
    teller_token = TellerAdmin.objects.filter(refresh_token=token).values()
    firstname = teller_token[0]['firstname']
    lastname = teller_token[0]['lastname']
    balance = teller_token[0]['balance']
    teller__acountid = teller_token[0]['teller_adminid']
    context = {
        'data': teller__acountid,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'token': token,
    }

    if teller__acountid == None:
        return render(request, 'teller_admin/teller-admin.html', {})
    else:
        return render(request, target_page, context)


def GetCustomerDetail(request):
    target_page = 'teller_transfer/transfer-customer.html'
    phoneno = request.POST.get('number')
    tellerid = request.POST.get('tellerid')
    customer_detail = CustomerAdmin.objects.filter(
        phoneno=int(phoneno)).values()
    telleradminid = TellerAdmin.objects.filter(
        teller_adminid=tellerid).values()
    id = telleradminid[0]['teller_adminid']
    firstname = telleradminid[0]['firstname']
    lastname = telleradminid[0]['lastname']
    balance = telleradminid[0]['balance']
    token = telleradminid[0]['refresh_token']
    customer_balance = customer_detail[0]['balance']
    customer_firstname = customer_detail[0]['firstname']
    customer_lastname = customer_detail[0]['lastname']
    num = customer_detail[0]['phoneno']
    if tellerid == None:
        return render(request, 'teller_admin/teller-admin.html', {})
    elif customer_balance == None or customer_balance == []:
        context = {
            'firstname': customer_firstname,
            'lastname': customer_lastname,
            'num': num,
            'id': id,
            'balance': 0,
            'T_firstname': firstname,
            'T_lastname': lastname,
            'T_balance': balance,
            'token': token,
        }

    else:
        context = {
            'firstname': customer_firstname,
            'lastname': customer_lastname,
            'num': num,
            'id': id,
            'balance': customer_balance,
            'T_firstname': firstname,
            'T_lastname': lastname,
            'T_balance': balance,
            'token': token,
        }
    return render(request, target_page, context)


def TransferToCustomer(request, token):
    target_page = 'teller_transfer/transfer-successful.html'
    transaction_options = request.POST.get('transaction')
    phoneno = request.POST.get('number')
    tellerid = request.POST.get('tellerid')
    amount = request.POST.get('amount')

    adminbal = TellerAdmin.objects.filter(refresh_token=token).values()
    tellerbalance = adminbal[0]['balance']
    teller_back_token = adminbal[0]['refresh_token']
    firstname = adminbal[0]['firstname']
    lastname = adminbal[0]['lastname']
    balance = adminbal[0]['balance']

    customer_balance = CustomerAdmin.objects.filter(phoneno=phoneno).values()
    customer_firstname = customer_balance[0]['firstname']
    context = {'data': 'Transfer Successful', 'token': teller_back_token}
    if transaction_options == "":
        target_page = 'teller_transfer/transfer-customer.html'
        phoneno = request.POST.get('number')
        tellerid = request.POST.get('tellerid')
        customer_detail = CustomerAdmin.objects.filter(
            phoneno=phoneno).values()
        telleradminid = TellerAdmin.objects.filter(
            refresh_token=token).values()
        id = telleradminid[0]['teller_adminid']
        T_firstname = telleradminid[0]['firstname']
        T_lastname = telleradminid[0]['lastname']
        T_balance = telleradminid[0]['balance']

        customer_balance = customer_detail[0]['balance']
        customer_firstname = customer_detail[0]['firstname']
        customer_lastname = customer_detail[0]['lastname']
        num = customer_detail[0]['phoneno']
        context = {
            'firstname': customer_firstname,
            'lastname': customer_lastname,
            'num': num,
            'id': id,
            'balance': customer_balance,
            'data': 'You did not choose from the transaction options!',
            'T_firstname': T_firstname,
            'T_lastname': T_lastname,
            'T_balance': T_balance,
            'token': teller_back_token,


        }

        return render(request, target_page, context)

    elif transaction_options == 'deposit':

        if tellerid == None:
            return render(request, 'teller_admin/teller-admin.html', {})

        elif tellerbalance == None or float(tellerbalance) == 0 or float(tellerbalance) < float(amount):
            context = {'data': 'Not enough balance'}
            return context
        tellerNewbal = float(tellerbalance) - float(amount)
        teller_transfer = TellerAdmin.objects.filter(
            teller_adminid=tellerid).update(balance=tellerNewbal)
        if teller_transfer:
            customer_balance = CustomerAdmin.objects.filter(
                phoneno=phoneno).values()
            customer_prev_bal = customer_balance[0]['balance']
            customer_accountid = customer_balance[0]['customer_accountid']

            if customer_prev_bal == None:
                customer_prev_bal = 0
                customer_new_bal = float(customer_prev_bal) + float(amount)
                CustomerAdmin.objects.filter(
                    phoneno=phoneno).update(balance=customer_new_bal)
            else:
                customer_new_bal = float(customer_prev_bal) + float(amount)
                CustomerAdmin.objects.filter(
                    phoneno=phoneno).update(balance=customer_new_bal)

            transfer = Transactions()
            transfer.deposit = amount
            transfer.fullname = customer_firstname
            transfer.teller_adminid = tellerid
            transfer.customer_accountid = customer_accountid
            transfer.phoneno = phoneno
            transfer.save()

            telleradminid = TellerAdmin.objects.filter(
                refresh_token=token).values()
            id = telleradminid[0]['teller_adminid']
            T_firstname = telleradminid[0]['firstname']
            T_lastname = telleradminid[0]['lastname']
            T_balance = telleradminid[0]['balance']

            context = {
                'data': 'Transfer Successful',
                'token': teller_back_token,
                'amount': amount,
                # 'T_Ref': T_Ref,
                # 'createdAt': createdAt,
                'name': customer_firstname,
                'tellerId': tellerid,
                'customerNum': phoneno,
                'T_firstname': firstname,
                'T_lastname': lastname,
                'T_balance': balance,

            }

    else:
        transaction_options == 'withdrawal'
        amount = request.POST.get('amount')
        trans_charger = float(amount) * 0.06
        transaction_charge = "{: .2f}".format(trans_charger)
        customer_balance = CustomerAdmin.objects.filter(
            phoneno=phoneno).values()
        customer_prev_bal = customer_balance[0]['balance']
        customer_accountid = customer_balance[0]['customer_accountid']

        if customer_prev_bal == None or float(customer_prev_bal) == 0 or float(customer_prev_bal) < float(amount):
            context = {'data': 'Not enough balance'}

            return render(request, target_page, context)

        else:
            totalAmoun = float(amount) + float(transaction_charge)
            customer_new_bal = float(customer_prev_bal) - float(totalAmoun)
            customer_transfer = CustomerAdmin.objects.filter(
                phoneno=phoneno).update(balance=customer_new_bal)

        if customer_transfer:
            tellerNewbal = float(tellerbalance) + float(amount)
            TellerAdmin.objects.filter(
                teller_adminid=tellerid).update(balance=tellerNewbal)

            bank_charge = BankAdmin.objects.filter(
                bank_adminid='950395193f214f0b826dcc4822bf165c').values()
            bank_charge_prev_bal = bank_charge[0]['charges']
            if bank_charge_prev_bal == None:
                bank_charge_prev_bal = 0
                current_charge = float(bank_charge_prev_bal) + \
                    float(transaction_charge)
                BankAdmin.objects.filter(
                    bank_adminid='950395193f214f0b826dcc4822bf165c').update(charges=current_charge)
            else:
                current_charge = float(bank_charge_prev_bal) + \
                    float(transaction_charge)
                BankAdmin.objects.filter(
                    bank_adminid='950395193f214f0b826dcc4822bf165c').update(charges=current_charge)

            transfer = Transactions()
            transfer.withdrawal = amount
            transfer.charges = float(transaction_charge)
            transfer.fullname = customer_firstname
            transfer.teller_adminid = tellerid
            transfer.customer_accountid = customer_accountid
            transfer.phoneno = phoneno
            transfer.save()

            charge = Charges()
            charge.withdrawal = amount
            charge.charges = float(transaction_charge)
            charge.fullname = customer_firstname
            charge.customer_accountid = customer_accountid
            charge.phoneno = phoneno
            charge.save()

            telleradminid = TellerAdmin.objects.filter(
                refresh_token=token).values()
            id = telleradminid[0]['teller_adminid']
            T_firstname = telleradminid[0]['firstname']
            T_lastname = telleradminid[0]['lastname']
            T_balance = telleradminid[0]['balance']

            context = {
                'data': 'Transfer Successful',
                'token': teller_back_token,
                'amount': amount,
                'charge': float(transaction_charge),
                'name': customer_firstname,
                'tellerId': tellerid,
                'customerNum': phoneno,
                'T_firstname': firstname,
                'T_lastname': lastname,
                'T_balance': balance,
                # 'T_Ref': T_Ref,
                # 'createdAt': createdAt,
            }
    return render(request, target_page, context)
