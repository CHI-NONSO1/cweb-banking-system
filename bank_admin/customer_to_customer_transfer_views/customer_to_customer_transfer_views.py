
from django.shortcuts import render
from bank_admin.models import BankAdmin, Charges, Transactions
from bank_admin.models import CustomerAdmin as Payer
from bank_admin.models import CustomerAdmin as Receiver


def GetReceiver(request, token):
    target_page = 'customer_to_customer_transfer/customer-account.html'
    payer_token = Payer.objects.filter(refresh_token=token).values()

    payer__acountid = payer_token[0]['customer_accountid']
    firstname = payer_token[0]['firstname']
    lastname = payer_token[0]['lastname']
    balance = payer_token[0]['balance']
    phoneno = payer_token[0]['phoneno']
    context = {
        'data': payer__acountid,
        'token': token,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
        'phoneno': phoneno,
    }
    if payer__acountid == None:
        return render(request, 'customer/my-bank.html', {})
    else:
        return render(request, target_page, context)


def GetReceiversDetail(request):
    target_page = 'customer_to_customer_transfer/transfer-customer.html'
    phoneno = request.POST.get('number')
    payerid = request.POST.get('payerid')
    receiver_detail = Receiver.objects.filter(phoneno=int(phoneno)).values()
    payer_id = Payer.objects.filter(
        customer_accountid=payerid).values()
    id = payer_id[0]['customer_accountid']
    payerToken = payer_id[0]['refresh_token']
    payerFirstName = payer_id[0]['firstname']
    payerLastName = payer_id[0]['lastname']
    PayerBalance = payer_id[0]['balance']
    PayerAccNum = payer_id[0]['phoneno']

    customer_firstname = receiver_detail[0]['firstname']
    customer_lastname = receiver_detail[0]['lastname']
    num = receiver_detail[0]['phoneno']
    if payer_id == None:
        return render(request, 'customer/my-bank.html', {})
    context = {
        'firstname': customer_firstname,
        'lastname': customer_lastname,
        'num': num,
        'id': id,
        'token': payerToken,
        'payerFirstName': payerFirstName,
        'payerLastName': payerLastName,
        'payerBalance': PayerBalance,
        'payerAccNum': PayerAccNum,
    }

    return render(request, target_page, context)


def TransferToReceiver(request):
    target_page = 'customer_to_customer_transfer/transfer-successful.html'

    phoneno = request.POST.get('number')
    payerID = request.POST.get('payerid')
    amount = request.POST.get('amount')
    if amount == '':
        target_page = 'customer_to_customer_transfer/transfer-customer.html'
        phoneno = request.POST.get('number')
        payerid = request.POST.get('payerid')
        receiver_detail = Receiver.objects.filter(
            phoneno=int(phoneno)).values()
        payer_id = Payer.objects.filter(
            customer_accountid=payerid).values()
        id = payer_id[0]['customer_accountid']
        payerToken = payer_id[0]['refresh_token']
        payerFirstName = payer_id[0]['firstname']
        payerLastName = payer_id[0]['lastname']
        PayerBalance = payer_id[0]['balance']
        PayerAccNum = payer_id[0]['phoneno']

        customer_firstname = receiver_detail[0]['firstname']
        customer_lastname = receiver_detail[0]['lastname']
        num = receiver_detail[0]['phoneno']
        context = {
            'firstname': customer_firstname,
            'lastname': customer_lastname,
            'num': num,
            'id': id,
            'token': payerToken,
            'payerFirstName': payerFirstName,
            'payerLastName': payerLastName,
            'payerBalance': PayerBalance,
            'payerAccNum': PayerAccNum,
            'error_message': 'You did not add an amount!',
        }
        return render(request, target_page, context)

    trans_charger = float(amount) * 0.06
    transaction_charge = "{: .2f}".format(trans_charger)

    payerbal = Payer.objects.filter(customer_accountid=payerID).values()
    payerbalance = payerbal[0]['balance']
    payer_firstname = payerbal[0]['firstname']
    payer_back_token = payerbal[0]['refresh_token']
    payer_phoneno = payerbal[0]['phoneno']
    receiver_balance = Receiver.objects.filter(phoneno=phoneno).values()
    customer_firstname = receiver_balance[0]['firstname']
    receiver_prev_bal = receiver_balance[0]['balance']
    receiver_accountid = receiver_balance[0]['customer_accountid']

    if receiver_prev_bal == None:
        receiver_prev_bal = 0
        receiver_new_bal = float(receiver_prev_bal) + float(amount)
    else:
        receiver_new_bal = float(receiver_prev_bal) + float(amount)

    receiver_transfer = Receiver.objects.filter(
        phoneno=phoneno).update(balance=receiver_new_bal)

    if receiver_transfer:
        amountPaid = float(amount) + float(transaction_charge)
        payerNewbal = float(payerbalance) - float(amountPaid)
        Payer.objects.filter(customer_accountid=payerID).update(
            balance=payerNewbal)

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

        payer = Transactions()
        payer.withdrawal = amount
        payer.charges = float(transaction_charge)
        payer.fullname = payer_firstname
        payer.teller_adminid = payerID
        payer.customer_accountid = payerID
        payer.phoneno = payer_phoneno
        payer.save()

        receiver = Transactions()
        receiver.deposit = amount
        receiver.fullname = customer_firstname
        receiver.teller_adminid = payerID
        receiver.customer_accountid = receiver_accountid
        receiver.phoneno = phoneno
        receiver.save()

        charge = Charges()
        charge.withdrawal = amount
        charge.charges = float(transaction_charge)
        charge.fullname = payer_firstname
        charge.customer_accountid = payerID
        charge.phoneno = payer_phoneno
        charge.save()

        payerInfo = Payer.objects.filter(customer_accountid=payerID).values()
        payerBalance = payerInfo[0]['balance']
        payerFirstName = payerInfo[0]['firstname']
        payerLastName = payerInfo[0]['lastname']
        payerAccNum = payerInfo[0]['phoneno']

        context = {
            'data': 'Transfer Successful',
            'token': payer_back_token,
            'amount': amount,
            'charge': float(transaction_charge),
            'name': customer_firstname,
            'senderId': payerID,
            'receiverNum': phoneno,
            'payerFirstName': payerFirstName,
            'payerLastName': payerLastName,
            'payerBalance': payerBalance,
            'payerAccNum': payerAccNum,
        }
        return render(request, target_page, context)
