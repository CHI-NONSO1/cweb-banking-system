from django.shortcuts import redirect, render
from bank_admin.models import TellerAdmin
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
import uuid
from django.utils import timezone


def Dashboard(request, teller):
    target_page = 'tellers/teller-admin.html'
    token = TellerAdmin.objects.filter(refresh_token=teller).values()
    teller_token = token[0]['refresh_token']
    firstname = token[0]['firstname']
    lastname = token[0]['lastname']
    phoneno = token[0]['phoneno']
    email = token[0]['email']
    image = token[0]['image']
    balance = token[0]['balance']
    context = {
        'token': teller_token,
        'firstname': firstname,
        'lastname': lastname,
        'phoneno': phoneno,
        'image': image,
        'balance': balance,
        'email': email
    }

    return render(request, target_page, context)


def TellerRegister(request):
    if request.method == 'POST':
        passwd = request.POST.get('password')
        teller = TellerAdmin()
        teller.firstname = request.POST.get('firstname')
        teller.lastname = request.POST.get('lastname')
        teller.email = request.POST.get('email')
        teller.phoneno = request.POST.get('phoneno')
        teller.password = make_password(passwd)
        teller.image = request.FILES.get('file')
        teller.balance = request.POST.get('balance')

        teller.save()

        return redirect('http://127.0.0.1:8000/teller-login')
    else:
        return render(request, 'tellers/teller-register.html', {'error_message': "Your password didn't match", })


def TellerLogin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = TellerAdmin.objects.get(email=email)
        us = TellerAdmin.objects.values('password')
        lo = list(us)[0]['password']
        usercheck = check_password(password, lo)
        if user and usercheck:
            tokenid = uuid.uuid4()
            TellerAdmin.objects.filter(email=email).update(
                refresh_token=tokenid)
            access = TellerAdmin.objects.filter(email=email).values()
            access_token = access[0]['refresh_token']

            return HttpResponseRedirect(reverse('bank_admin:teller-admin', args=[str(access_token)],))

        else:
            return render(request, 'tellers/teller-login.html', {'error_message': "You ."})
    else:

        return render(request, 'tellers/teller-login.html', {})


def TellerLogout(request, token):
    TellerAdmin.objects.filter(refresh_token=token).update(
        refresh_token='None')

    return redirect('http://127.0.0.1:8000/teller-login', {})


def TellerAdminAccountDetail(request, token):
    target_page = 'tellers/teller-admin-account-detail.html'
    access_token = TellerAdmin.objects.filter(refresh_token=token).values()
    admin_token = access_token[0]['refresh_token']
    email = access_token[0]['email']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']

    context = {
        'token': admin_token,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'balance': balance,
    }
    return render(request, target_page, context)


def TellerAdminUpdateAccount(request):
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

        TellerAdmin.objects.filter(email=email).update(
            city=city,
            address=address,
            job_title=job_title,
            # image='images/' + str(new_img),
            updatedAt=timezone.now())

        return HttpResponseRedirect(reverse('bank_admin:teller-admin-update-status', args=[str(token)],))

    else:
        return render(request, 'teller/teller-admin-account-detail.html', {'error_message': "Something went wrong!", })


def TellerAdminUpdateAccountStatus(request, token):
    target_page = 'tellers/teller-admin-update-status.html'
    access_token = TellerAdmin.objects.filter(refresh_token=token).values()
    admin_token = access_token[0]['refresh_token']
    email = access_token[0]['email']
    city = access_token[0]['city']
    address = access_token[0]['address']
    job_title = access_token[0]['job_title']
    firstname = access_token[0]['firstname']
    lastname = access_token[0]['lastname']
    balance = access_token[0]['balance']

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


    }
    return render(request, target_page, context)
