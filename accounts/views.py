from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, PasswordVerificationAdminForm, SecurityQuestionsForm, PasswordForm, SignUpForm, IndivdualUserForm, IndivdualDoctorForm, HospitalForm, NursingHomeForm, ModuleMasterForm, ContactForm, PasswordVerificationForm, AddServices,pharamcy, CouponForm, EventregisteruserForm,Eventregistertable
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import SecurityQuestions, ModuleMaster, Contact, LaboratoryPreDefine, LaboratoryEmpty, CustomUser, AddOnServices,pharamcytab, LaboratoryModule, Coupon, Webregister, Eventregisterationuser
from django.http import Http404
from django.http import Http404
from django.contrib import messages
from django.http import JsonResponse
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from .token_generator import account_activation_token
from django.core.mail import EmailMessage
import datetime
import json
from .decorators import superadmin_required
from profiles.models import IndivdualDoctorProfile, NursingHomeProfile, HospitalProfile, IndivdualUserProfile
from django.conf import settings

#from django.contrib.auth.forms import SetPasswordForm

@csrf_exempt
def aboutus(request):
    return render(request, 'About_Us.html')

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')

        if form.is_valid():
            if form.save():
                return redirect('/contact', messages.success(request, 'Thank you for contacting Us. Our team will contact you as soon as earliest.', 'alert-success'))
            else:
                return redirect('/contact', messages.error(request, 'Something went wrong!', 'alert-danger'))
        else:
            return redirect('/contact', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = ContactForm()
        return render(request, "Contact_Us.html", {'form':form})

@login_required
@csrf_exempt
def contact_master(request):
    module = Contact.objects.all()
    return render(request, "Contact_Us_List.html", {'module': module})

@csrf_exempt
def home(request):
    return render(request, "index.html", {})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/existing_module_master', messages.success(request, 'Your account has been activated successfully!', 'alert-success'))
    else:
        return redirect('/register', messages.error(request, 'Activation link is invalid!', 'alert-danger'))

#https://www.google.com/settings/security/lesssecureapps

@csrf_exempt
def register(request):
    next = request.GET.get('next')
    if 'individualdoctor' in request.POST:

        form1 = IndivdualDoctorForm(request.POST)
        if form1.is_valid():
            # form2 = HospitalForm(request.POST)
            # if form2.is_valid():

            user = form1.save(commit=False)

            usecode = request.POST['usecode']
            list_display = ['is_individual', 'is_hdc_individual', 'is_hdc_hospital', 'is_hdc_nursing_home']
            code_check = Coupon.objects.filter(code=usecode, profileChoices='is_hdc_individual').exists()


            if (code_check == True):

                code_to_count = CustomUser.objects.filter(usecode=usecode, is_hdc_individual=True)
                counted_values = code_to_count.count()

                Coupon_count = Coupon.objects.get(code=usecode, profileChoices='is_hdc_individual')
                counted_in_models = Coupon_count.count_value
                Check_date = Coupon_count.endDate
                if (counted_values <= counted_in_models and (
                        str(Check_date) >= str(datetime.date.today().strftime('20%y-%m-%d')))):

                    password = form1.cleaned_data.get('password')
                    type = form1.cleaned_data.get('type_of_doctor')

                    user.type_of_doctor = type
                    user.set_password(password)
                    user.is_hdc_individual = True
                    user.save()
                    email_subject = 'Welcome To Health Perigon!'
                    valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                    date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                    type1 = "HDC - Individual Doctor"
                    message = render_to_string('activate_account.html', {
                        'user': user,
                        'type': type1,
                        'valid_till': valid_till,
                    })
                    to_email = form1.cleaned_data.get('email')
                    phone_no = form1.cleaned_data.get('phone_no')
                    email = EmailMessage(email_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    payload = {}
                    payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                    payload['content-type'] = "application/json"
                    payload['mobiles'] = phone_no
                    payload['flow_id'] = "5efada07d6fc05445570a4f2"
                    payload['ID'] = user.special_id
                    url = "https://api.msg91.com/api/v5/flow/"
                    response = requests.post(url, json=payload)
                    data = response.json()
                    login(request, user)
                    if request.user.is_authenticated:
                        IndivdualDoctorProfile.objects.create(user=request.user)
                    if next:
                        return redirect(next)
                    return redirect('profile_individual_doctor')
            else:
                return redirect('/register', messages.error(request, 'Invalid code', 'alert-danger'))


        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register', messages.error(request, 'Form is not valid', 'alert-danger'))


    else:
        form1 = IndivdualDoctorForm(request.POST)

    if 'hospital' in request.POST:
        form2 = HospitalForm(request.POST)

        if form2.is_valid():

            usecode = request.POST['usecode']
            list_display = ['is_individual', 'is_hdc_individual', 'is_hdc_hospital', 'is_hdc_nursing_home']
            code_check = Coupon.objects.filter(code=usecode, profileChoices='is_hdc_hospital').exists()

            if (code_check == True):
                code_to_count = CustomUser.objects.filter(usecode=usecode, is_hdc_hospital=True)
                counted_values = code_to_count.count()
                Coupon_count = Coupon.objects.get(code=usecode, profileChoices='is_hdc_hospital')
                counted_in_models = Coupon_count.count_value
                Check_date = Coupon_count.endDate
                if (counted_values <= counted_in_models and (
                        str(Check_date) >= str(datetime.date.today().strftime('20%y-%m-%d')))):

                    user = form2.save(commit=False)
                    password = form2.cleaned_data.get('password')

                    payment = request.POST.get('yesno')
                    user.payment = payment
                    user.set_password(password)
                    user.is_hdc_hospital = True
                    user.save()
                    email_subject = 'Welcome To Health Perigon!'
                    valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                    date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                    type1 = "HDC - Hospital"
                    message = render_to_string('activate_account.html', {
                        'user': user,
                        'type': type1,
                        'valid_till': valid_till,
                    })
                    to_email = form2.cleaned_data.get('email')
                    phone_no = form2.cleaned_data.get('phone_no')
                    email = EmailMessage(email_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    payload = {}
                    payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                    payload['content-type'] = "application/json"
                    payload['mobiles'] = phone_no
                    payload['flow_id'] = "5efada07d6fc05445570a4f2"
                    payload['ID'] = user.special_id
                    url = "https://api.msg91.com/api/v5/flow/"
                    response = requests.post(url, json=payload)
                    data = response.json()
                    login(request, user)
                    if request.user.is_authenticated:
                        HospitalProfile.objects.create(user=request.user)
                    if next:
                        return redirect(next)
                    return redirect('profile_hospital')
            elif (code_check==False):
                return redirect('/register', messages.error(request, 'Invalid code', 'alert-danger'))

        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form2 = HospitalForm(request.POST)

    if 'nursinghome' in request.POST:
        form3 = NursingHomeForm(request.POST)
        if form3.is_valid():
            usecode = request.POST['usecode']
            list_display = ['is_individual', 'is_hdc_individual', 'is_hdc_hospital', 'is_hdc_nursing_home']
            code_check = Coupon.objects.filter(code=usecode, profileChoices='is_hdc_nursing_home').exists()


            if code_check == True:
                # code_to_count = CustomUser.objects.filter(usecode=usecode,is_hdc_nursing_home=True).exists()
                code_to_count = CustomUser.objects.filter(usecode=usecode, is_hdc_nursing_home=True)

                counted_values = code_to_count.count()

                Coupon_count = Coupon.objects.get(code=usecode, profileChoices='is_hdc_nursing_home')
                counted_in_models = Coupon_count.count_value

                Check_date = Coupon_count.endDate
                if (counted_values <= counted_in_models and
                    str(Check_date) >= str(datetime.date.today().strftime('20%y-%m-%d'))):


                    user = form3.save(commit=False)
                    password = form3.cleaned_data.get('password')
                    user.set_password(password)
                    user.is_hdc_nursing_home = True

                    user.save()
                    email_subject = 'Welcome To Health Perigon!'
                    valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                    date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                    type1 = "HDC - Nursing Home"
                    message = render_to_string('activate_account.html', {
                        'user': user,
                        'type': type1,
                        'valid_till': valid_till,
                    })
                    to_email = form3.cleaned_data.get('email')
                    phone_no = form3.cleaned_data.get('phone_no')
                    email = EmailMessage(email_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    payload = {}
                    payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                    payload['content-type'] = "application/json"
                    payload['mobiles'] = phone_no
                    payload['flow_id'] = "5efada07d6fc05445570a4f2"
                    payload['ID'] = user.special_id
                    url = "https://api.msg91.com/api/v5/flow/"
                    response = requests.post(url, json=payload)
                    data = response.json()
                    login(request, user)
                    if request.user.is_authenticated:
                        NursingHomeProfile.objects.create(user=request.user)
                    if next:
                        return redirect(next)
                    return redirect('profile_nursing_home')
            else:
                return redirect('/register', messages.error(request, 'Invalid code', 'alert-danger'))

        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form3 = NursingHomeForm(request.POST)

    if 'individualuser' in request.POST:
        form = IndivdualUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            usecode = form.cleaned_data.get('usecode')


            code_check = Coupon.objects.filter(code=usecode)

            code_to_count = CustomUser.objects.filter(usecode=usecode).count()
            count = Coupon.objects.filter(code=usecode).values_list('count_value',flat=True)
            check_date = Coupon.objects.filter(code=usecode).values_list('endDate', flat=True)

            if (code_check.exists()==True and code_to_count<=count[0] and (str(check_date[0]) >= str(datetime.date.today().strftime('20%y-%m-%d')))):

                user.set_password(password)
                user.is_individual = True

                user.save()
                email_subject = 'Welcome To Health Perigon!'
                valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                type1 = "HDC - Individual User"
                message = render_to_string('activate_account.html', {
                    'user': user,
                    'type': type1,
                    'valid_till': valid_till,
                })
                to_email = form.cleaned_data.get('email')
                phone_no = form.cleaned_data.get('phone_no')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.send()
                payload = {}
                payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                payload['content-type'] = "application/json"
                payload['mobiles'] = phone_no
                payload['flow_id'] = "5efada07d6fc05445570a4f2"
                payload['ID'] = user.special_id
                url = "https://api.msg91.com/api/v5/flow/"
                response = requests.post(url, json=payload)
                data = response.json()

                login(request, user)
                if request.user.is_authenticated:
                    IndivdualUserProfile.objects.create(user=request.user)
                if next:
                    return redirect(next)
                return redirect('profile_individual_user')
            else:
                return redirect('/register', messages.error(request, 'Invalid code', 'alert-danger'))
        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = IndivdualUserForm()

    return render(request, "Register.html", {'form': form, 'form1': form1, 'form2': form2, 'form3': form3})

@csrf_exempt
def register1(request):
    next = request.GET.get('next')
    if 'individualdoctor' in request.POST:

        form1 = IndivdualDoctorForm(request.POST)
        if form1.is_valid():
            # form2 = HospitalForm(request.POST)
            # if form2.is_valid():

            user = form1.save(commit=False)

            usecode = request.POST['usecode']
            list_display = ['is_individual', 'is_hdc_individual', 'is_hdc_hospital', 'is_hdc_nursing_home']
            code_check = Coupon.objects.filter(code=usecode, profileChoices='is_hdc_individual').exists()


            if (code_check == True):

                code_to_count = CustomUser.objects.filter(usecode=usecode, is_hdc_individual=True)
                counted_values = code_to_count.count()

                Coupon_count = Coupon.objects.get(code=usecode, profileChoices='is_hdc_individual')
                counted_in_models = Coupon_count.count_value
                Check_date = Coupon_count.endDate
                if (counted_values <= counted_in_models and (
                        str(Check_date) >= str(datetime.date.today().strftime('20%y-%m-%d')))):

                    password = form1.cleaned_data.get('password')
                    type = form1.cleaned_data.get('type_of_doctor')

                    user.type_of_doctor = type
                    user.set_password(password)
                    user.is_hdc_individual = True
                    user.save()
                    email_subject = 'Welcome To Health Perigon!'
                    valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                    date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                    type1 = "HDC - Individual Doctor"
                    message = render_to_string('activate_account.html', {
                        'user': user,
                        'type': type1,
                        'valid_till': valid_till,
                    })
                    to_email = form1.cleaned_data.get('email')
                    phone_no = form1.cleaned_data.get('phone_no')
                    email = EmailMessage(email_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    payload = {}
                    payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                    payload['content-type'] = "application/json"
                    payload['mobiles'] = phone_no
                    payload['flow_id'] = "5efada07d6fc05445570a4f2"
                    payload['ID'] = user.special_id
                    url = "https://api.msg91.com/api/v5/flow/"
                    response = requests.post(url, json=payload)
                    data = response.json()
                    login(request, user)
                    if request.user.is_authenticated:
                        IndivdualDoctorProfile.objects.create(user=request.user)
                    if next:
                        return redirect(next)
                    return redirect('Custom_user_list')
            else:
                return redirect('/register1', messages.error(request, 'Invalid code', 'alert-danger'))


        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register1', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register1', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register1', messages.error(request, 'Form is not valid', 'alert-danger'))


    else:
        form1 = IndivdualDoctorForm(request.POST)

    if 'hospital' in request.POST:
        form2 = HospitalForm(request.POST)

        if form2.is_valid():

            usecode = request.POST['usecode']
            list_display = ['is_individual', 'is_hdc_individual', 'is_hdc_hospital', 'is_hdc_nursing_home']
            code_check = Coupon.objects.filter(code=usecode, profileChoices='is_hdc_hospital').exists()

            if (code_check == True):
                code_to_count = CustomUser.objects.filter(usecode=usecode, is_hdc_hospital=True)
                counted_values = code_to_count.count()
                Coupon_count = Coupon.objects.get(code=usecode, profileChoices='is_hdc_hospital')
                counted_in_models = Coupon_count.count_value
                Check_date = Coupon_count.endDate
                if (counted_values <= counted_in_models and (
                        str(Check_date) >= str(datetime.date.today().strftime('20%y-%m-%d')))):

                    user = form2.save(commit=False)
                    password = form2.cleaned_data.get('password')

                    payment = request.POST.get('yesno')
                    user.payment = payment
                    user.set_password(password)
                    user.is_hdc_hospital = True
                    user.save()
                    email_subject = 'Welcome To Health Perigon!'
                    valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                    date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                    type1 = "HDC - Hospital"
                    message = render_to_string('activate_account.html', {
                        'user': user,
                        'type': type1,
                        'valid_till': valid_till,
                    })
                    to_email = form2.cleaned_data.get('email')
                    phone_no = form2.cleaned_data.get('phone_no')
                    email = EmailMessage(email_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    payload = {}
                    payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                    payload['content-type'] = "application/json"
                    payload['mobiles'] = phone_no
                    payload['flow_id'] = "5efada07d6fc05445570a4f2"
                    payload['ID'] = user.special_id
                    url = "https://api.msg91.com/api/v5/flow/"
                    response = requests.post(url, json=payload)
                    data = response.json()
                    login(request, user)
                    if request.user.is_authenticated:
                        HospitalProfile.objects.create(user=request.user)
                    if next:
                        return redirect(next)
                    return redirect('Custom_user_list')
            elif (code_check==False):
                return redirect('/register1', messages.error(request, 'Invalid code', 'alert-danger'))

        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register1', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register1', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register1', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form2 = HospitalForm(request.POST)

    if 'nursinghome' in request.POST:
        form3 = NursingHomeForm(request.POST)
        if form3.is_valid():
            usecode = request.POST['usecode']
            list_display = ['is_individual', 'is_hdc_individual', 'is_hdc_hospital', 'is_hdc_nursing_home']
            code_check = Coupon.objects.filter(code=usecode, profileChoices='is_hdc_nursing_home').exists()


            if code_check == True:
                # code_to_count = CustomUser.objects.filter(usecode=usecode,is_hdc_nursing_home=True).exists()
                code_to_count = CustomUser.objects.filter(usecode=usecode, is_hdc_nursing_home=True)

                counted_values = code_to_count.count()

                Coupon_count = Coupon.objects.get(code=usecode, profileChoices='is_hdc_nursing_home')
                counted_in_models = Coupon_count.count_value

                Check_date = Coupon_count.endDate
                if (counted_values <= counted_in_models and
                    str(Check_date) >= str(datetime.date.today().strftime('20%y-%m-%d'))):


                    user = form3.save(commit=False)
                    password = form3.cleaned_data.get('password')
                    user.set_password(password)
                    user.is_hdc_nursing_home = True

                    user.save()
                    email_subject = 'Welcome To Health Perigon!'
                    valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                    date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                    type1 = "HDC - Nursing Home"
                    message = render_to_string('activate_account.html', {
                        'user': user,
                        'type': type1,
                        'valid_till': valid_till,
                    })
                    to_email = form3.cleaned_data.get('email')
                    phone_no = form3.cleaned_data.get('phone_no')
                    email = EmailMessage(email_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    payload = {}
                    payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                    payload['content-type'] = "application/json"
                    payload['mobiles'] = phone_no
                    payload['flow_id'] = "5efada07d6fc05445570a4f2"
                    payload['ID'] = user.special_id
                    url = "https://api.msg91.com/api/v5/flow/"
                    response = requests.post(url, json=payload)
                    data = response.json()
                    login(request, user)
                    if request.user.is_authenticated:
                        NursingHomeProfile.objects.create(user=request.user)
                    if next:
                        return redirect(next)
                    return redirect('Custom_user_list')
            else:
                return redirect('/register1', messages.error(request, 'Invalid code', 'alert-danger'))

        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register1', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register1', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register1', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form3 = NursingHomeForm(request.POST)

    if 'individualuser' in request.POST:
        form = IndivdualUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            usecode = form.cleaned_data.get('usecode')


            code_check = Coupon.objects.filter(code=usecode)

            code_to_count = CustomUser.objects.filter(usecode=usecode).count()
            count = Coupon.objects.filter(code=usecode).values_list('count_value',flat=True)
            check_date = Coupon.objects.filter(code=usecode).values_list('endDate', flat=True)

            if (code_check.exists()==True and code_to_count<=count[0] and (str(check_date[0]) >= str(datetime.date.today().strftime('20%y-%m-%d')))):

                user.set_password(password)
                user.is_individual = True

                user.save()
                email_subject = 'Welcome To Health Perigon!'
                valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                type1 = "HDC - Individual User"
                message = render_to_string('activate_account.html', {
                    'user': user,
                    'type': type1,
                    'valid_till': valid_till,
                })
                to_email = form.cleaned_data.get('email')
                phone_no = form.cleaned_data.get('phone_no')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.send()
                payload = {}
                payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                payload['content-type'] = "application/json"
                payload['mobiles'] = phone_no
                payload['flow_id'] = "5efada07d6fc05445570a4f2"
                payload['ID'] = user.special_id
                url = "https://api.msg91.com/api/v5/flow/"
                response = requests.post(url, json=payload)
                data = response.json()

                login(request, user)
                if request.user.is_authenticated:
                    IndivdualUserProfile.objects.create(user=request.user)
                if next:
                    return redirect(next)
                return redirect('Custom_user_list')
            else:
                return redirect('/register1', messages.error(request, 'Invalid code', 'alert-danger'))
        else:
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('/register1', messages.error(request, 'Email already Exists!', 'alert-danger'))
            elif CustomUser.objects.filter(phone_no=phone_no).exists():
                return redirect('/register1', messages.error(request, 'Phone Number already Exists!', 'alert-danger'))
            else:
                return redirect('/register1', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = IndivdualUserForm()

    return render(request, "register1.html", {'form': form, 'form1': form1, 'form2': form2, 'form3': form3})

@superadmin_required
@csrf_exempt
def existing_module_master(request):
    if request.user.is_authenticated:
        #user = ModuleMaster.objects.get(user=request.user)
        #module = ModuleMaster.objects.filter(user=user.user)
        module = ModuleMaster.objects.all()
        return render(request, "Subscription_Master-Existing_Module_Master.html", {'module': module})


@superadmin_required
@csrf_exempt
def create_module_master(request):
    #user = ModuleMaster.objects.get(user=request.user)
    if request.method == 'POST':
        form = ModuleMasterForm(request.POST)
        if form.is_valid():
            #module_name = form.cleaned_data.get('module_name')
            #module_code = form.cleaned_data.get('module_code')
            #no_of_patients = form.cleaned_data.get('no_of_patients')
            #web_space = form.cleaned_data.get('web_space')
            #amount = form.cleaned_data.get('amount')
            #cgst = form.cleaned_data.get('cgst')
            #sgst = form.cleaned_data.get('sgst')
            #gst = form.cleaned_data.get('gst')
            #total_amount = form.cleaned_data.get('total_amount')
            #ModuleMaster.objects.create(user = request.user, module_name = module_name, module_code = module_code, no_of_patients = no_of_patients, web_space = web_space, amount = amount, cgst = cgst, sgst = sgst, gst = gst, total_amount = total_amount)
            #ModuleMaster.objects.create(user= request.user)
            if form.save():
                return redirect('/create_module_master', messages.success(request, 'Module is successfully created.', 'alert-success'))
            else:
                return redirect('/create_module_master', messages.error(request, 'Module is not saved', 'alert-danger'))
        else:
            return redirect('/create_module_master', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = ModuleMasterForm()
        return render(request, 'Subscription_Master-Create_Module_Master.html', {'form':form})

@superadmin_required
@csrf_exempt
def edit_module_master(request, module_id):
    module = ModuleMaster.objects.get(id=module_id)
    if request.POST:
        form = ModuleMasterForm(request.POST, instance=module)
        if form.is_valid():
            if form.save():
                return redirect('/existing_module_master', messages.success(request, 'Module is successfully updated.', 'alert-success'))
            else:
                return redirect('/existing_module_master', messages.error(request, 'Module is not saved', 'alert-danger'))
        else:
            return redirect('/existing_module_master', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = ModuleMasterForm(instance=module)
        return render(request, 'Subscription_Master-Edit_Module_Master.html', {'form':form})

@superadmin_required
@csrf_exempt
def destroy_module_master(request, module_id):
    module = ModuleMaster.objects.get(id=module_id)
    module.delete()
    return redirect('/existing_module_master', messages.success(request, 'Module is successfully deleted.', 'alert-success'))

@csrf_exempt
def password_reset_admin(request):
    form = PasswordForm(request.POST or None)
    form1 = PasswordVerificationAdminForm(request.POST or None)

    if request.method == 'POST':
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')

        #check = SecurityQuestions.objects.get(id=1)   #change it when adding security question
    else:
        form = PasswordForm()
        form1 = PasswordVerificationAdminForm()
    return render(request,"forget_password_admin.html", {"form": form, "form1":form1})

@csrf_exempt
def send_otp_admin(request):
    if request.method == "GET":
        email = request.GET.get('email')
        if CustomUser.objects.filter(email=email).exists():
            reg_email = CustomUser.objects.get(email=email)
            phone_no = reg_email.phone_no
        #url = "https://api.msg91.com/api/v5/otp?authkey=95631AQvoigMsq5ec52866P1&template_id=5ec52d2dd6fc050944666272&mobile=+919702221660&invisible=1&otp=OTP to send and verify. If not sent, OTP will be generated.&userip=IPV4 User IP&email=Email ID"
        url = 'https://api.msg91.com/api/v5/otp?authkey=95631AQvoigMsq5ec52866P1&template_id=5ec52d2dd6fc050944666272&mobile='+"+91"+str(phone_no)+'&invisible=1&userip=IPV4 User IP&email=Email ID'
        response = requests.request("GET",url)
        data = response.json()
        data_json = {"error" : False, "errorMessage" : "OTP Sent to your registered phone number"}
    else:
        data_json = {"error" : True, "errorMessage" : "Email not registered"}
    return JsonResponse(data_json)


@csrf_exempt
def verify_otp_admin(request):
    if request.method == "POST":
        otptxt = request.POST.get('phone_no')
        url = 'https://api.msg91.com/api/v5/otp/verify?mobile=+919702221660&otp='+str(otptxt)+'&authkey=95631AQvoigMsq5ec52866P1'
        response = requests.request("POST",url)
        data = response.json()
        data_json = {"error" : False, "errorMessage" : "OTP verified"}
    else:
        data_json = {"error" : True, "errorMessage" : "Fail to verify"}
    return JsonResponse(data_json)




@csrf_exempt
def password_reset(request):
    form = PasswordForm(request.POST or None)
    form1 = PasswordVerificationForm(request.POST or None)

    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        phone_no = request.POST.get('phone_no')
        check = SecurityQuestions.objects.get(id=1)   #change it when adding security question
        if check.answer == answer:
            data_json = {"error" : False, "errorMessage" : "Correct Answer"}
            return JsonResponse(data_json, safe=False)
        else:
            data_json = {"error" : True, "errorMessage" : "Incorrect Answer"}
            return JsonResponse(data_json, safe=False)
    else:
        form = PasswordForm()
        form1 = PasswordVerificationForm()
    return render(request,"forget_password.html", {"form": form, "form1":form1})

@csrf_exempt
def change_password(request):
    form = PasswordForm()
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            data_json = {"error" : True, "errorMessage" : "Password Mismatch"}
            return JsonResponse(data_json, safe=False)
        else:

            request.user.password = make_password(password)
            request.user.save()
            data_json = {"error" : False, "errorMessage" : "Password Changed"}
            return JsonResponse(data_json, safe=False)
    return render(request,"forget_password.html", {"form": form})

@csrf_exempt
def change_password_admin(request):
    form = PasswordForm()
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        if password != password_confirm:
            data_json = {"error" : True, "errorMessage" : "Password Mismatch"}
            return JsonResponse(data_json, safe=False)
        else:
            data1 = CustomUser.objects.get(email=email)
            data1.password = make_password(password)
            data1.save()
            data_json = {"error" : False, "errorMessage" : "Password Changed"}
            return JsonResponse(data_json, safe=False)
    return render(request,"forget_password_admin.html", {"form": form})

@csrf_exempt
def send_otp(request):
    if request.method == "GET":
        #url = "https://api.msg91.com/api/v5/otp?authkey=95631AQvoigMsq5ec52866P1&template_id=5ec52d2dd6fc050944666272&mobile=+919702221660&invisible=1&otp=OTP to send and verify. If not sent, OTP will be generated.&userip=IPV4 User IP&email=Email ID"
        url = "https://api.msg91.com/api/v5/otp?authkey=95631AQvoigMsq5ec52866P1&template_id=5ec52d2dd6fc050944666272&mobile=+917400395192&invisible=1&userip=IPV4 User IP&email=Email ID"
        response = requests.request("GET",url)
        data = response.json()
        data_json = {"error" : False, "errorMessage" : "OTP Sent to your phone"}
    else:
        data_json = {"error" : True, "errorMessage" : "Failed to send OTP"}
    return JsonResponse(data_json)


@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        otptxt = request.POST.get('phone_no')
        url = 'https://api.msg91.com/api/v5/otp/verify?mobile=+919702221660&otp='+str(otptxt)+'&authkey=95631AQvoigMsq5ec52866P1'
        response = requests.request("POST",url)
        data = response.json()
        data_json = {"error" : False, "errorMessage" : "OTP verified"}
    else:
        data_json = {"error" : True, "errorMessage" : "Fail to verify"}
    return JsonResponse(data_json)

@csrf_exempt
def login_view(request):
    next = request.GET.get("next")
    check = CustomUser.objects.get(id=1)
    if check.last_login != None:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if not user:
                return redirect('/accounts/login/', messages.error(request, 'Username or password is incorrect', 'alert-danger'))
            login(request, user)
            if next:
                return redirect(next)
            if request.user.is_superuser:
                return redirect('contact_master')
            elif request.user.is_hdc_individual:
                return redirect('profile_individual_doctor')
            elif request.user.is_individual:
                return redirect('profile_individual_user')
            elif request.user.is_hdc_hospital:
                return redirect('profile_hospital')
            elif request.user.is_hdc_nursing_home:
                return redirect('profile_nursing_home')
        return render(request, "login.html", {'form': form})
    else:
        form = UserLoginForm(request.POST or None)
        form1 = SecurityQuestionsForm(request.POST or None)
        if form.is_valid() and form1.is_valid():
            form1.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if not user:
                return redirect('/accounts/login_superadmin/', messages.error(request, 'Username or password is incorrect', 'alert-danger'))
            login(request, user)
            if next:
                return redirect(next)
            return redirect('contact_master')
        return render(request, "login.html", {'form': form, 'form1':form1})


@csrf_exempt
def login_view_admin(request):
    next = request.GET.get("next")
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        if not user:
            return redirect('/accounts/login/', messages.error(request, 'Username or password is incorrect', 'alert-danger'))
        login(request, user)
        if next:
            return redirect(next)
        if request.user.is_superuser:
            return redirect('contact_master')
        elif request.user.is_hdc_individual:
            return redirect('profile_individual_doctor')
        elif request.user.is_individual:
            return redirect('profile_individual_user')
        elif request.user.is_hdc_hospital:
            return redirect('profile_hospital')
        elif request.user.is_hdc_nursing_home:
            return redirect('profile_nursing_home')
    return render(request, "login_admin.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def addservice(request):
    if request.method=='POST':
        reg = AddServices(request.POST)
        if reg.is_valid():
            if reg.save():
                return redirect('/addonservice', messages.success(request, 'Module is successfully updated.', 'alert-success'))
            else:
                return redirect('/addonservice', messages.error(request, 'Module is not saved', 'alert-danger'))
        else:
            return redirect('/addonservice', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        reg = AddServices()
        return render(request, 'addservice.html', {'reg':reg})

@csrf_exempt
def addonservice(request):
    module = AddOnServices.objects.all()
    return render(request,"addservicetable.html",{'module':module})

@csrf_exempt
def destroyonservice(request, module_id):
    module = AddOnServices.objects.get(id=module_id)
    module.delete()
    return redirect('/addonservice', messages.success(request, 'Module is successfully deleted.', 'alert-success'))

@csrf_exempt
def pharmacytable(request):
    module = pharamcytab.objects.all()
    return render(request,'pharmacytable.html',{'module':module})


@csrf_exempt
def pharmacy(request):
    if request.method =='POST':
        reg=pharamcy(request.POST)
        
        if reg.is_valid():

            if reg.save():
                 return redirect('/pharmacytable', messages.success(request, 'Service is successfully updated.', 'alert-success'))
            else:
                return redirect('/pharmacytable', messages.error(request, 'Service is not saved', 'alert-danger'))
        else:
            return redirect('/pharmacytable', messages.error(request, 'Service is not valid', 'alert-danger'))
    else:
        reg=pharamcy()
        return render(request, 'pharmacy master.html', {'reg': reg})

@csrf_exempt
def destroypharamcy(request, module_id):
    module = pharamcytab.objects.get(id=module_id)
    module.delete()
    return redirect('/pharmacytable', messages.success(request, 'Module is successfully deleted.', 'alert-success'))

@csrf_exempt
def laboratory_insertion(request):
    data = request.POST.get("data")
    investigation_name = request.POST.get("investigation_name")
    synonyms = request.POST.get("synonyms")
    important_note = request.POST.get("important_note")
    check = request.POST.get("check")
    dict_data = json.loads(data)
    intial_data = LaboratoryModule(investigation_name=investigation_name, synonyms=synonyms, important_note=important_note)
    intial_data.save()
    name = LaboratoryModule.objects.get(investigation_name=investigation_name)
    if check == "predefine_dropdown":
        try:
            select_dropdown_list = request.POST.get("select_dropdown_list")
            select = request.POST.get("select")
            initial_data2 = LaboratoryPreDefine(investigation=name, select_dropdown_list=select_dropdown_list, select=select)
            initial_data2.save()
            data_json = {"error" : False, "errorMessage" : "Data Added Sucessfully"}
            return JsonResponse(data_json, safe=False)
        except:
            data_json = {"error" : True, "errorMessage" : "Failed To Add Data"}
            return JsonResponse(data_json, safe=False)

    elif check == "empty_text":
        try:
            for dict_single in dict_data:
                initial_data3 = LaboratoryEmpty(investigation=name, from_age=dict_single['from_age'], to_age=dict_single['to_age'], gender=dict_single['gender'], conventional=dict_single['conventional'], umo1=dict_single['umo1'], umo2=dict_single['umo2'], conversion_factor=dict_single['conversion_factor'], high1=dict_single['high1'], low1=dict_single['low1'], high2 = dict_single['high2'], low2 = dict_single['low2'])
                initial_data3.save()
            data_json = {"error" : False, "errorMessage" : "Data Added Sucessfully"}
            return JsonResponse(data_json, safe=False)
        except:
            data_json = {"error" : True, "errorMessage" : "Failed To Add Data"}
            return JsonResponse(data_json, safe=False)

@superadmin_required
@csrf_exempt
def laboratory(request):
    return render(request, 'laboratory.html')

@superadmin_required
@csrf_exempt
def laboratory_edit(request, module_id):
    data = LaboratoryModule.objects.get(id=module_id)
    data1 = LaboratoryPreDefine.objects.filter(investigation=module_id).first()
    data2 = LaboratoryEmpty.objects.filter(investigation=module_id)
    return render(request,'laboratory_edit.html',{"data":data,"data1":data1,"data2":data2})

@csrf_exempt
def laboratory_update(request):
    data1=request.POST.get("data")
    investigation_name=request.POST.get("investigation_name")
    synonyms=request.POST.get("synonyms")
    important_note=request.POST.get("important_note")
    select_dropdown_list=request.POST.get("select_dropdown_list")
    select=request.POST.get("select")
    base_id=request.POST.get("base_id")
    pre_id=request.POST.get("pre_id")
    dict_data=json.loads(data1)
    try:
        base=LaboratoryModule.objects.get(id=base_id)
        base.investigation_name = investigation_name
        base.synonyms = synonyms
        base.important_note = important_note
        base.save()
        if pre_id != "":
            pre = LaboratoryPreDefine.objects.get(id=pre_id)
            pre.select_dropdown_list = select_dropdown_list
            pre.select = select
            pre.save()
        else:
            for dic_single in dict_data:
                data=LaboratoryEmpty.objects.get(id=dic_single['id'])
                data.from_age=dic_single['from_age']
                data.to_age=dic_single['to_age']
                data.conventional=dic_single['conventional']
                data.umo1=dic_single['umo1']
                data.umo2=dic_single['umo2']
                data.conversion_factor=dic_single['conversion_factor']
                data.high1=dic_single['high1']
                data.low1=dic_single['low1']
                data.high2=dic_single['high2']
                data.low2=dic_single['low2']
                data.save()
        data_json={"error":False,"errorMessage":"Updated Successfully"}
        return JsonResponse(data_json,safe=False)
    except:
        data_json={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(data_json,safe=False)

@csrf_exempt
def lob(request):
    module=LaboratoryModule.objects.all()
    return render(request,'laboratorytable.html',{'module':module})  


@csrf_exempt
def destroylaboratory(request, module_id):
    module = LaboratoryModule.objects.get(id=module_id)
    module.delete()
    return redirect('/laboratorytable', messages.success(request, 'Successfully deleted.', 'alert-success'))

@csrf_exempt
def edit_service(request, module_id):
    module1 = AddOnServices.objects.get(id=module_id)
    if request.POST:
        reg = AddServices(request.POST, instance=module1)
        if reg.is_valid():
            if reg.save():
                return redirect('/addservice', messages.success(request, 'Module is successfully updated.', 'alert-success'))
            else:
                return redirect('/addservice', messages.error(request, 'Module is not saved', 'alert-danger'))
        else:
            return redirect('/addservice', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        reg = AddServices(instance=module1)
        return render(request, 'edit_service.html', {'reg':reg})

@csrf_exempt
def edit_pharmacy(request, module_id):
    module = pharamcytab.objects.get(id=module_id)
    if request.POST:
        reg = pharamcy(request.POST, instance=module)
        if reg.is_valid():
            if reg.save():
                return redirect('/pharmacy', messages.success(request, 'Module is successfully updated.', 'alert-success'))
            else:
                return redirect('/pharmacy', messages.error(request, 'Module is not saved', 'alert-danger'))
        else:
            return redirect('/pharmacy', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        reg = pharamcy(instance=module)
        return render(request, 'edit_pharmacy.html', {'reg':reg})


@csrf_exempt
def update_database(request):
    reg =labo(request.POST or None)
    if request.method == 'POST':
        froms = request.POST.get('froms')
        to= request.POST.get('to')
        gender = request.POST.get('gender')
        umo1 = request.POST.get('umo1')
        umo2 = request.POST.get('muo2')
        conversationfactor = request.POST.get('conversationfactor')
        refrencerange = request.POST.get('refrencerange')
        high = request.POST.get('high')
        return render(request,'sample2.html',{"reg":reg})
    else:
        reg = labo()
        return render(request,'sample2.html',{"reg":reg})

@csrf_exempt
def labo2(request):
    module = Empty.objects.all()
    return render(request,'sample.html',{'module':module})

@csrf_exempt
def add_individual_user(request):
    if request.method == 'POST':
        form = IndivdualUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("../")
    else:
        form = IndivdualUserForm()
    return render(request,'add_user.html',{'form':form})


@csrf_exempt
def User_creation(request):
    if request.method == 'POST':
        form = IndivdualDoctorForm(request.POST)
        first_name = request.POST.get('first_name')

        if form.is_valid():
            if form.save():
                return redirect('/User_creation', messages.success(request, 'Thank you for contacting Us. Our team will contact you as soon as earliest.', 'alert-success'))
            else:
                return redirect('/User_creation', messages.error(request, 'Something went wrong!', 'alert-danger'))
        else:
            return redirect('/User_creation', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = IndivdualDoctorForm()
        return render(request, "User_creation.html", {'form': form})



@csrf_exempt
def account_status_change(request):
    status = request.GET
    some_list = CustomUser.objects.filter(special_id=status['id']).values_list('is_active', flat=True)
    if some_list[0] == True:
        some_list = CustomUser.objects.filter(special_id=status['id']).update(is_active=False)
    elif some_list[0] == False:
        some_list = CustomUser.objects.filter(special_id=status['id']).update(is_active=True)
    return HttpResponse()


@csrf_exempt
def Custom_user_list(request):
    custmore_obj = CustomUser.objects.all().values()
    context = {
        'customers':custmore_obj
    }

    return render(request,'custom_user_list.html',context)

@csrf_exempt
def coupon_code_list(request):
    coupon_obj = Coupon.coupon.all().values_list('code', flat=True)              #,'profileChoices'
    final_data = []

    for i in coupon_obj:
        coup_count = CustomUser.objects.filter(usecode=i).values_list('email', flat=True)
        coup_count_use = len(coup_count)
        coupon_obj1 = list(Coupon.objects.filter(code=i).values())
        a = dict(used_number=coup_count_use)
        coupon_obj1[0].update(a)
        final_data.append(coupon_obj1)
    done=[]
    for l in final_data:
        done.append(l[0])

    context = {
        'coupon':done
    }
    return render(request,'coupon_code_list.html',context)


@csrf_exempt
def custom_account_status_change(request):
    status = request.GET
    some_list = CustomUser.objects.filter(special_id=status['id']).values_list('is_active', flat=True)
    if some_list[0] == True:
        some_list = CustomUser.objects.filter(special_id=status['id']).update(is_active=False)
    elif some_list[0] == False:
        some_list = CustomUser.objects.filter(special_id=status['id']).update(is_active=True)
    return HttpResponse()

@csrf_exempt
def Coupon_status_change(request):
    status = request.GET
    some_list = Coupon.objects.filter(code=status['id']).values_list('active')
    res = [lis[0] for lis in some_list]

    if res[0] == True:
        some_list =Coupon.objects.filter(code=status['id']).update(active=False)
    elif res[0] == False:
        some_list = Coupon.objects.filter(code=status['id']).update(active=True)
    return HttpResponse()

@csrf_exempt
def add_coupon(request):
    form = CouponForm()
    return render(request, 'added_coupon.html',{'form':form})

@csrf_exempt
def Coupon_to_create(request):
    if request.method == "POST" and request.is_ajax():
        code = request.POST.get('code')

        check_code = Coupon.objects.filter(code=code)

        if request.POST.get('profileChoices') not in Coupon.objects.filter(code=code):
            form = CouponForm(request.POST)
            if form.is_valid():
                form.save()
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=400)
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def Add_streaming_link(request):
    streaming_link = request.POST.get("streaming_link")
    eventtitle = request.POST.get("eventtitle")
    eventtype = request.POST.get("eventtype")
    targetaudiance = request.POST.get("targetaudiance")


    query = Webregister.objects.filter(eventtitle=eventtitle,eventtype=eventtype,targetaudiance=targetaudiance).exists()
    if query == True:
        query = Webregister.objects.filter(eventtitle=eventtitle,eventtype=eventtype,targetaudiance=targetaudiance).update(streaming_link=streaming_link)
    else:
        return JsonResponse({"success": False}, status=400)


    return JsonResponse({"success": True}, status=200)

@csrf_exempt
def partner_visibility(request):

    if request.method == 'POST':

        form = EventregisteruserForm(request.POST, request.FILES) #, instance=obj
        if form.is_valid():

            header_eventimage = form.cleaned_data.get('header_eventimage')
            footer_eventimage = form.cleaned_data.get('footer_eventimage')
            streaming_header = form.cleaned_data.get('streaming_header')
            streaming_leftpanel = form.cleaned_data.get('streaming_leftpanel')
            streaming_rightpanel = form.cleaned_data.get('streaming_rightpanel')


            types = ['.jpg', '.png', '.jpeg','.PNG']

            import pathlib
            if header_eventimage:
                a = pathlib.Path(str(header_eventimage)).suffix

                if a not in types:
                    return redirect('/partner_visibility',
                                    messages.error(request, 'Please proper format for header_eventimage', 'alert-danger'))

                if header_eventimage:
                    if header_eventimage.size > 1000 * 100:  # 41937
                        return redirect('/partner_visibility', messages.error(request, 'Images should have proper configuration for header_eventimage', 'alert-danger'))

            if footer_eventimage:
                b = pathlib.Path(str(footer_eventimage)).suffix

                if b not in types:
                    return redirect('/partner_visibility',
                                    messages.error(request, 'Please proper format for footer_eventimage', 'alert-danger'))

                if footer_eventimage:
                    if footer_eventimage.size > 1000 * 100:  # 41937
                        return redirect('/partner_visibility', messages.error(request, 'Images should have proper configuration for footer_eventimage ', 'alert-danger'))

            if streaming_header:
                c = pathlib.Path(str(streaming_header)).suffix

                if c not in types:
                    return redirect('/partner_visibility',
                                    messages.error(request, 'Please proper format for streaming_header', 'alert-danger'))

                if streaming_header:
                    if streaming_header.size > 1000 * 100:  # 41937
                        return redirect('/partner_visibility', messages.error(request, 'Images should have proper configuration for streaming_header', 'alert-danger'))

            if streaming_leftpanel:
                d = pathlib.Path(str(streaming_leftpanel)).suffix

                if d not in types:
                    return redirect('/partner_visibility',
                                    messages.error(request, 'Please proper format for streaming_leftpanel', 'alert-danger'))

                if streaming_leftpanel:
                    if streaming_leftpanel.size > 700 * 200:  # 41937
                        return redirect('/partner_visibility', messages.error(request, 'Images should have proper configuration for streaming_leftpanel', 'alert-danger'))
            if streaming_rightpanel:
                e = pathlib.Path(str(streaming_rightpanel)).suffix

                if e not in types:
                    return redirect('/partner_visibility',
                                    messages.error(request, 'Please proper format for streaming_leftpanel', 'alert-danger'))

                if streaming_rightpanel:
                    if streaming_rightpanel.size > 700 * 200:  # 41937
                        return redirect('/partner_visibility', messages.error(request, 'Images should have proper configuration for streaming_rightpanel', 'alert-danger'))



            if form.save():

                return redirect('/partner_visibility',
                                messages.success(request, 'visibility is successfully submitted.', 'alert-success'))
            else:
                return redirect('/partner_visibility', messages.error(request, 'Images should have proper configuration', 'alert-danger'))

        else:
            return redirect('/partner_visibility', messages.error(request, 'visibilityis not valid', 'alert-danger'))
    else:

        form = EventregisteruserForm()
        return render(request, 'partner_visibility.html', {'form': form})

@csrf_exempt
def event_visibility(request):
    if request.method == 'POST':
        mail_id = request.POST['email']
        form1 = Eventregistertable(request.POST)
        if form1.is_valid():

            form1.save()
        aa = Webregister.objects.get(email=mail_id)
        obj = Eventregisterationuser.objects.create(webregister=aa)
        return partner_visibility(obj)


@csrf_exempt
def eventregister(request):
    if request.method == 'POST':
        form = Eventregistertable(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/eventtable',
                                messages.success(request, 'Event is successfully updated.', 'alert-success'))
            else:
                return redirect('/eventtable', messages.error(request, 'Event is not saved', 'alert-danger'))
        else:
            return redirect('/eventtable', messages.error(request, 'Event is not valid', 'alert-danger'))
    else:
        form = Eventregistertable()
        return render(request,'event.html', {'form': form})


@csrf_exempt
def home_event(request):
    events = Webregister.objects.all()
    context={
        'events':events
    }

    return render(request,"index_event.html",context)


@csrf_exempt
def eventtable(request):
     module=Webregister.objects.all().values()
     return render(request,"eventtable.html",{'module':module})


# @csrf_exempt
# def event_register_form(request,module_id):
#     module = Webregister.objects.get(id=module_id) #42
#     object = Eventregisterationuser.objects.get(webregister=module)
#
#
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#
#         if form.is_valid():
#
#             form.save()
#             messages.success(request, 'Event Created Successfully.')
#     else:
#         form = SignUpForm()
#     return render(request,'home_user.html',{'form':form,'object':object})

@csrf_exempt
def registerlink(request, module_id):
    module = Webregister.objects.get(id=module_id)
    if request.POST:
        form = Eventregistertable(request.POST, instance=module)
        if form.is_valid():
            if form.save():
                return redirect('/eventregister', messages.success(request, 'Event is successfully updated.', 'alert-success'))
            else:
                return redirect('/eventregister', messages.error(request, 'Event is not saved', 'alert-danger'))
        else:
            return redirect('/eventregister', messages.error(request, 'Event is not valid', 'alert-danger'))
    else:
        form = Eventregistertable(instance=module)
        return render(request, 'editevent.html', {'form':form})

@csrf_exempt
def editevent(request, module_id): #,new_module
    module = Webregister.objects.get(id=module_id)

    new_module = Eventregisterationuser.objects.get(webregister=module)

    if request.POST:
        form = Eventregistertable(request.POST,instance=module)
        form1 = EventregisteruserForm(request.POST,request.FILES,instance=new_module)
        if form.is_valid():
            form.save()
            if form1.is_valid():
                form1.save()
                return redirect('/eventtable/', messages.error(request, 'successfully updated', 'alert-danger'))
        else:
            return redirect('/editevent/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = Eventregistertable(instance=module)
        form1 = EventregisteruserForm(instance=new_module)
        p_image = Eventregisterationuser.objects.filter(webregister=module).values()[0]

        p_image.update(form1.data)
        return render(request, 'editevent.html', {'form':form,'form1':p_image})

@csrf_exempt
def destroyevent(request, module_id):
    module = Webregister.objects.get(id=module_id)
    module.delete()
    return redirect('/eventtable', messages.success(request, 'Event is successfully deleted.', 'alert-success'))

@csrf_exempt
def partner_and_event_register(request):
    if request.method == 'POST':
        form = Eventregistertable(request.POST)
        if form.is_valid():
            form.save()
            aa = Webregister.objects.latest('id')
            aa.register_link = 'www.healthperigon.net/'+ str(Webregister.objects.latest('id'))
            aa.save()
            obj = Eventregisterationuser.objects.create(webregister=aa)
            form1 = EventregisteruserForm(request.POST, request.FILES, instance=obj)


            if form1.is_valid():
                header_eventimage = form.cleaned_data.get('header_eventimage')
                footer_eventimage = form.cleaned_data.get('footer_eventimage')
                streaming_header = form.cleaned_data.get('streaming_header')
                streaming_leftpanel = form.cleaned_data.get('streaming_leftpanel')
                streaming_rightpanel = form.cleaned_data.get('streaming_rightpanel')
                types = ['.jpg', '.png', '.jpeg', '.PNG']

                import pathlib
                if header_eventimage:
                    a = pathlib.Path(str(header_eventimage)).suffix

                    if a not in types:
                        return redirect('/partner_and_event_register',
                                        messages.error(request, 'Please proper format for header_eventimage','alert-danger'))
                        if header_eventimage:
                            if header_eventimage.size > 1000 * 100:  # 41937
                                return redirect("/partner_and_event_register", messages.error(request, 'Images should have proper configuration for footer_eventimage ', 'alert-danger'))

                    if footer_eventimage:
                        b = pathlib.Path(str(footer_eventimage)).suffix

                        if b not in types:
                            return redirect('/partner_and_event_register',
                                            messages.error(request, 'Please proper format for footer_eventimage',
                                                           'alert-danger'))

                        if footer_eventimage:
                            if footer_eventimage.size > 1000 * 100:  # 41937
                                return redirect('/partner_and_event_register', messages.error(request,
                                                                                      'Images should have proper configuration for footer_eventimage ',
                                                                                      'alert-danger'))

                    if streaming_header:
                        c = pathlib.Path(str(streaming_header)).suffix

                        if c not in types:
                            return redirect('/partner_and_event_register',
                                            messages.error(request, 'Please proper format for streaming_header',
                                                           'alert-danger'))

                        if streaming_header:
                            if streaming_header.size > 1000 * 100:  # 41937
                                return redirect('/partner_and_event_register', messages.error(request,
                                                                                      'Images should have proper configuration for streaming_header',
                                                                                      'alert-danger'))

                    if streaming_leftpanel:
                        d = pathlib.Path(str(streaming_leftpanel)).suffix

                        if d not in types:
                            return redirect('/partner_and_event_register',
                                            messages.error(request, 'Please proper format for streaming_leftpanel',
                                                           'alert-danger'))

                        if streaming_leftpanel:
                            if streaming_leftpanel.size > 200 * 700:  # 41937
                                return redirect('/partner_and_event_register', messages.error(request,
                                                                                      'Images should have proper configuration for streaming_leftpanel',
                                                                                      'alert-danger'))
                    if streaming_rightpanel:
                        e = pathlib.Path(str(streaming_rightpanel)).suffix

                        if e not in types:
                            return redirect('/partner_and_event_register',
                                            messages.error(request, 'Please proper format for streaming_leftpanel',
                                                           'alert-danger'))

                        if streaming_rightpanel:
                            if streaming_rightpanel.size > 200 * 700:  # 41937
                                return redirect('/partner_and_event_register', messages.error(request,
                                                                                      'Images should have proper configuration for streaming_rightpanel',
                                                                                      'alert-danger'))



                form1.save()
                return redirect('/partner_and_event_register',
                                messages.success(request, 'Visibility Created Successfully.', 'alert-success'))


            return redirect('/partner_and_event_register',
                                messages.success(request, 'Event Created Successfully.', 'alert-success'))

        else:
            return redirect('/partner_and_event_register', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = Eventregistertable()
        form1 = EventregisteruserForm()
        return render(request,'create_partner.html', {'form': form,'form1':form1})

@csrf_exempt		
def show_events(request):
    objects = Eventregisterationuser.objects.filter(webregister__created_on__gt=datetime.datetime.now())
    past_event = Eventregisterationuser.objects.filter(webregister__ends_on__lt=datetime.datetime.now())
    return render(request,'Events.html',{'objects':objects, 'past_event':past_event})
    
    
@csrf_exempt
def event_register_form(request, module_id):
    module = Webregister.objects.get(id=module_id)
    link = module.register_link
    print(module.register_link, 'reglink')  # www.healthperigon.net/2
    object = Eventregisterationuser.objects.get(webregister=module)

    check_category = Webregister.objects.get(id=module_id)
    target = check_category.targetaudiance
    title = check_category.eventtitle

    if request.method == "POST":
        if 'doctor' in request.POST:
            print(request.POST, "type_of_doctor")
            form = IndivdualDoctorForm(request.POST)
            email = request.POST.get('email')
            type_of_doctor = request.POST.get('type_of_doctor')
            print(type_of_doctor,'type_of_doctor')
            print(form.errors, 'form')

            if form.is_valid():

                user = form.save(commit=False)
                email = form.cleaned_data.get('email')

                print(email, 'email')
                password = form.cleaned_data.get('password')
                confirm_password = form.cleaned_data.get('confirm_password')

                if password != confirm_password:
                    return redirect('/event_register_form/' + str(module_id),
                                    messages.error(request, "Password Should Match "), 'alert-danger')

                print("yes")
                type = form.cleaned_data.get('type_of_doctor')
                user.type_of_doctor = type
                user.set_password(password)
                user.is_hdc_individual = True
                user.register_link = link
                user.save()
                email_subject = 'Welcome To Health Perigon!'
                valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                type1 = "HDC - Individual Doctor"
                message = render_to_string('activate_account.html', {
                    'user': user,
                    'type': type1,
                    'valid_till': valid_till,
                    'link': link,
                })
                to_email = form.cleaned_data.get('email')
                phone_no = form.cleaned_data.get('phone_no')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.send()
                payload = {}
                payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                payload['content-type'] = "application/json"
                payload['mobiles'] = phone_no
                # payload['register_link'] = link
                payload['flow_id'] = "5efada07d6fc05445570a4f2"
                payload['ID'] = user.special_id
                url = "https://api.msg91.com/api/v5/flow/"
                response = requests.post(url, json=payload)
                data = response.json()
                print(data, 'data')

                try:
                    # IndivdualDoctorProfile.objects.create(user=request.user)
                    # print("done")
                    new_user = CustomUser.objects.get(email=to_email)
                    obj = IndivdualDoctorProfile.objects.create(user=new_user)  # ,register_link=link
                    print("obj", obj)
                except:
                    pass

                # +str(module_id)

                return redirect('/show_events/', messages.success(request, '{}{}{}'.format(
                    "You have succesfully registered for this ", title, " event"), 'alert-success'))
            else:
                return redirect('/event_register_form/' + str(module_id),
                                messages.success(request, ("Form is invalid"), 'alert-danger'))
        if 'individual' in request.POST:
            print('individual')
            form1 = IndivdualUserForm(request.POST)
            username = request.POST.get('email')
            print(form1.errors, 'error')
            if form1.is_valid():
                user = form1.save(commit=False)

                password = form1.cleaned_data.get('password')
                confirm_password = form1.cleaned_data.get('confirm_password')

                if password != confirm_password:
                    return redirect('/event_register_form/' + str(module_id),
                                    messages.error(request, "Password Should Match "), 'alert-danger')
                user.set_password(password)
                user.is_individual = True
                user.register_link = link
                user.save()
                email_subject = 'Welcome To Health Perigon!'
                valid_till = (datetime.datetime.now() + datetime.timedelta(days=364)).date()
                date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
                type1 = "HDC - Individual User"
                message = render_to_string('activate_account.html', {
                    'user': user,
                    'type': type1,
                    'valid_till': valid_till,
                    'link': link,
                })
                to_email = form1.cleaned_data.get('email')
                phone_no = form1.cleaned_data.get('phone_no')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.send()
                payload = {}
                payload['authkey'] = "95631AQvoigMsq5ec52866P1"
                payload['content-type'] = "application/json"
                payload['mobiles'] = phone_no
                payload['flow_id'] = "5efada07d6fc05445570a4f2"
                payload['ID'] = user.special_id
                url = "https://api.msg91.com/api/v5/flow/"
                response = requests.post(url, json=payload)
                data = response.json()
                print(data, 'data')
                try:
                    new_user = CustomUser.objects.get(email=to_email)
                    obj = IndivdualUserProfile.objects.create(user=new_user)
                    print("obj", obj)
                except:
                    pass

                return redirect('/show_events/', messages.success(request, '{}{}{}'.format(
                    "You have succesfully registered for this ", title, " event"), 'alert-success'))
            else:
                return redirect('/event_register_form/' + str(module_id),
                                messages.success(request, "Form is invalid", 'alert-success'))

        if 'loginForm' in request.POST:
            print("login")
            form2 = UserLoginForm(request.POST)
            print(request.POST, 'form2')
            if form2.is_valid():
                username = form2.cleaned_data['username']
                password = form2.cleaned_data['password']  # loginForm

                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    print("fine work")
                    for_link = CustomUser.objects.filter(email=username).update(register_link=link)
                    print(for_link, 'linkkk')
                return redirect('/show_events/', messages.success(request, '{}{}{}'.format(
                    "You have succesfully registered for this ", title, " event"), 'alert-success'))

            else:
                return redirect('/event_register_form/' + str(module_id),
                                messages.success(request, "Form is invalid", 'alert-success'))

    else:
        form = IndivdualDoctorForm()
        form1 = IndivdualUserForm()
        form2 = UserLoginForm()

        return render(request, 'home_user.html',
                      {'form': form, 'object': object, 'target': target, 'form1': form1, 'form2': form2})

@csrf_exempt
def password_reset_user_for_event(request):
    form = PasswordForm(request.POST or None)
    form1 = PasswordVerificationAdminForm(request.POST or None)

    if request.method == 'POST':
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')

        # check = SecurityQuestions.objects.get(id=1)   #change it when adding security question
    else:
        form = PasswordForm()
        form1 = PasswordVerificationAdminForm()
    return render(request,"password_reset_user_for_event.html", {"form": form, "form1":form1})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        form_login = UserLoginForm(request.POST)
        if form_login.is_valid():

            username = form_login.cleaned_data['username']

            password = form_login.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request,user)

                # return HttpResponseRedirect('sign_up')
                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse({"success": False}, status=400)
        else:

            form_login = UserLoginForm()
        return redirect('/sign_up/')


# @csrf_exempt
# def streaming(request, id):
#     module = Webregister.objects.get(id=id)
#     object = Eventregisterationuser.objects.get(webregister=module)
#     return render(request, "video_streaming.html", {'module':module,'object':object})
    
def streaming(request, id):
    module = Webregister.objects.get(id=id)
    object = Eventregisterationuser.objects.get(webregister=module)
    link_check = module.register_link
    print(module.register_link, 'register_link')  # www.healthperigon.net/2
    some_auth = CustomUser.objects.filter(email=request.user, register_link=link_check)
    print(some_auth,'auth')
    check_auth = CustomUser.objects.filter(email=request.user, register_link=link_check).exists()
    print(check_auth,"check_auth")
    if check_auth == False:
        return redirect('/event_register_form/' + str(id))
    else:
        return render(request, "video_streaming.html", {'module': module, 'object': object})