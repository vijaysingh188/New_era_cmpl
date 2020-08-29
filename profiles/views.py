from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import IndivdualDoctorProfileForm, UserForm, NursingHomeProfileForm, HospitalProfileForm, IndivdualUserProfileForm,UserAddedbyIndividualDoctorform,UserAddedbyIndividualDoctorform_record,  PasswordForm, PasswordUserForm, UserLoginForm
from accounts.models import CustomUser
from .models import IndivdualDoctorProfile, NursingHomeProfile, HospitalProfile, IndivdualUserProfile, Individual_Doctor_User
from accounts.decorators import individual_required, hdc_individual_required, hdc_hospital_required, hdc_nursing_home_required,useraddebyindvidualdoctor
from .models import UserAddedbyIndividualDoctor
from django.core.mail import EmailMessage
import datetime
import json
from django.template.loader import render_to_string
import requests
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from django.http import HttpResponse, JsonResponse

@hdc_individual_required
@csrf_exempt
def individual_doctor(request):
    if request.user.is_authenticated:
        user_profile = IndivdualDoctorProfile.objects.get(user=request.user)
    if request.POST:
        userform = UserForm(request.POST, instance = request.user)
        profileform = IndivdualDoctorProfileForm(request.POST,request.FILES, instance = user_profile)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user

        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
            profile.save()

            return redirect('/profile_individual_doctor', messages.success(request, 'Profile Updated Successfully.', 'alert-success'))
        else:
            return redirect('/profile_individual_doctor', messages.error(request, 'Profile is not Valid', 'alert-danger'))
    else:
        form1 = UserForm(instance = request.user)
        form2 = IndivdualDoctorProfileForm(instance = user_profile)
    return render(request,'Profile_HDC_Individual_Doctor.html', {'form1':form1, 'form2': form2})



@individual_required
@csrf_exempt
def individual_user(request):
    if request.user.is_authenticated:
        user_profile = IndivdualUserProfile.objects.get(user=request.user)
    if request.POST:
        userform = UserForm(request.POST, instance = request.user)
        profileform = IndivdualUserProfileForm(request.POST, instance = user_profile)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save(commit=False)
            user.save()
            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('/profile_individual_user', messages.success(request, 'Profile Updated Successfully.', 'alert-success'))
        else:
            return redirect('/profile_individual_user', messages.error(request, 'Profile is not Valid', 'alert-danger'))
    else:
        form1 = UserForm(instance = request.user, initial={'country':'IN'})
        form2 = IndivdualUserProfileForm(instance = user_profile)
    return render(request, "Profile_Individual.html", {'form1':form1, 'form2': form2})

@hdc_hospital_required
@csrf_exempt
def hospital(request):
    if request.user.is_authenticated:
        user_profile = HospitalProfile.objects.get(user=request.user)
    if request.POST:
        userform = UserForm(request.POST, instance = request.user)
        profileform = HospitalProfileForm(request.POST,request.FILES, instance = user_profile)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user

        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
            profile.save()

            return redirect('/profile_hospital', messages.success(request, 'Profile Updated Successfully.', 'alert-success'))
        else:
            return redirect('/profile_hospital', messages.error(request, 'Profile is not Valid', 'alert-danger'))
    else:
        form1 = UserForm(instance = request.user)
        form2 = HospitalProfileForm(instance = user_profile)
    return render(request, "Profile_HDC_Hospital.html", {'form1':form1, 'form2': form2})

@hdc_nursing_home_required
@csrf_exempt
def nursing_home(request):
    if request.user.is_authenticated:
        user_profile = NursingHomeProfile.objects.get(user=request.user)
    if request.POST:
        userform = UserForm(request.POST, instance = request.user)
        profileform = NursingHomeProfileForm(request.POST,request.FILES, instance = user_profile)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            profile = profileform.save(commit=False)
            profile.user = user

        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
            profile.save()

            return redirect('/profile_nursing_home', messages.success(request, 'Profile Updated Successfully.', 'alert-success'))
        else:
            return redirect('/profile_nursing_home', messages.error(request, 'Profile is not Valid', 'alert-danger'))
    else:
        form1 = UserForm(instance = request.user)
        form2 = NursingHomeProfileForm(instance = user_profile)
    return render(request, "Profile_HDC_Nursing_Home.html", {'form1':form1, 'form2': form2})



@csrf_exempt
def individual_doctor_user_creation(request):
    if request.method=='GET': 
        return render(request, 'User_Creation.html')
    elif request.method=='POST':
        form_data=request.POST
        a=dict(type_of_doctor=form_data['type_of_doctor'],title=form_data['title'],first_name=form_data['first_name'],middle_name=form_data['middle_name'],last_name=form_data['last_name'],phone_no=form_data['phone_no'],email=form_data['email'])
        form=UserAddedbyIndividualDoctorform(request.POST)
        try:
            number = "+91"+form_data['phone_no']
            carrier._is_mobile(number_type(phonenumbers.parse(number)))
        except Exception as e:
            
            return HttpResponse(json.dumps({"status":"IM","message":"Invalid Number"}),content_type="application/json")
        if CustomUser.objects.filter(phone_no=form_data['phone_no']).exists():
            return HttpResponse(json.dumps({"status":"MNE","message":"Phone Number already Exists!"}),content_type="application/json")
                
        elif CustomUser.objects.filter(email=form_data['email']).exists():
            return HttpResponse(json.dumps({"status":"EmailE","message":"Email already Exists!"}),content_type="application/json")
        
        else:
            if form.is_valid():  
                form.save()
            email_id=form.cleaned_data.get('email')
            phone_no=form.cleaned_data.get('phone_no')
            type_of_doctor=form.cleaned_data.get('type_of_doctor')

            u=CustomUser.objects.get(email=email_id)
            u.set_password('HP@1234')
            u.useraddebyindvidualdoctor=True
            if type_of_doctor=='DF':
                type_of_doctor='Junior Doctor'
                u.type_of_doctor=type_of_doctor
            else:
                type_of_doctor='Front Desk'
                u.type_of_doctor=type_of_doctor
            u.save()
            Individual_Doctor_User.objects.create(user=request.user,emails=email_id)
            u2=list(CustomUser.objects.filter(email=request.user).values('date_joined'))
            source=u2[0]['date_joined'].strftime("%Y-%m-%d %H:%M:%S.%f")
            source=datetime.datetime.strptime(source, '%Y-%m-%d %H:%M:%S.%f')
            email_subject = 'Welcome To Health Perigon!'
            valid_till = (source + datetime.timedelta(days=364)).date()
            date = json.dumps(valid_till, indent=4, sort_keys=True, default=str)
            message = render_to_string('User_activate_account.html', {
                'user': u,
                'type': type_of_doctor,
                'valid_till' : valid_till,
            })
            
            email = EmailMessage(email_subject, message, to=[email_id])
            email.content_subtype = 'html'
            email.send()
            payload = {}
            payload['authkey'] = "95631AQvoigMsq5ec52866P1"
            payload['content-type'] = "application/json"
            payload['mobiles'] = phone_no
            payload['flow_id'] = "5efada07d6fc05445570a4f2"
            payload['ID'] = u.special_id
            url = "https://api.msg91.com/api/v5/flow/"
            response = requests.post(url, json=payload)
            new_user=CustomUser.objects.get(email=email_id,)
            if request.user.is_authenticated:
                UserAddedbyIndividualDoctor.objects.create(user= new_user,type_of_doctor=form_data['type_of_doctor'])
            from django.http import HttpResponseRedirect
            return HttpResponse(json.dumps({"status":"success","message":"Profile Updated Successfully."}),content_type="application/json")
            



@useraddebyindvidualdoctor
@csrf_exempt
def useraddebyindvidualdoctor(request):

    typeofdoc= CustomUser.objects.filter(email=request.user).values_list('type_of_doctor',flat=True)
    if request.user.is_authenticated:
        user_profile = UserAddedbyIndividualDoctor.objects.get(user=request.user)
    if request.POST and request.is_ajax:
        userform = UserAddedbyIndividualDoctorform(request.POST, instance = request.user)
        a=UserAddedbyIndividualDoctor.objects.get(user=request.user)

        profileform = UserAddedbyIndividualDoctorform_record(request.POST,request.FILES, instance = a)

        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            email_id=userform.cleaned_data.get('email')
            type_of_doctor=userform.cleaned_data.get('type_of_doctor')

            u=CustomUser.objects.get(email=email_id)
            if type_of_doctor=='DF':
                u.type_of_doctor='Junior Doctor'
            else:
                u.type_of_doctor='Front Desk'
            u.save()
            profile = profileform.save(commit=False)
            profile.user = user
            phone_no=profileform.cleaned_data.get('phone_no2')
            gender=profileform.cleaned_data.get('gender')
            reg_no_number=profileform.cleaned_data.get('reg_no_number')
            CON=profileform.cleaned_data.get('country')
            if typeofdoc[0]=='Junior Doctor':
                if (gender=='Select Gender'):
                    return HttpResponse(json.dumps({"status":"GNS","message":"Select gender"}),content_type="application/json")
                elif len(reg_no_number)==0:
                    return HttpResponse(json.dumps({"status":"reg_no_number","message":"Please Enter Medical Council Registration Number"}),content_type="application/json")

                elif len(phone_no)!=0:  
                    try:
                        number = "+91"+phone_no
                        carrier._is_mobile(number_type(phonenumbers.parse(number)))
                        profile.save()
                        return HttpResponse(json.dumps({"status":"success","message":"Profile Updated Successfully"}),content_type="application/json")
                    except Exception as e:
                        return HttpResponse(json.dumps({"status":"IM","message":"Invalid Number"}),content_type="application/json")
                elif 'picture' in request.FILES:
                    
                    profile.picture = request.FILES['picture']
                    # profile.picture = request.FILES['pictureof_certificate']
                    profile.save()
                    return HttpResponse(json.dumps({"status":"success","message":"Profile Updated Successfully"}),content_type="application/json")
                else:
                    profile.save()
                    return HttpResponse(json.dumps({"status":"success","message":"Profile Updated Successfully"}),content_type="application/json")
            else:
                
                if (gender=='Select Gender'):
                        return HttpResponse(json.dumps({"status":"GNS","message":"Select gender"}),content_type="application/json")
                elif len(phone_no)!=0:  
                    try:
                        number = "+91"+phone_no
                        carrier._is_mobile(number_type(phonenumbers.parse(number)))
                    except Exception as e:
                        return HttpResponse(json.dumps({"status":"IM","message":"Invalid Number"}),content_type="application/json")
                else:
                    profile.save()
                    return HttpResponse(json.dumps({"status":"success","message":"Profile Updated Successfully"}),content_type="application/json")
        else:
            return redirect('/useraddebyindvidualdoctor', messages.error(request, 'Profile is not Valid', 'alert-danger'))
    else:
        a=UserAddedbyIndividualDoctor.objects.get(user=request.user)
        aa=CustomUser.objects.filter(email=request.user).values()
        form1 = UserAddedbyIndividualDoctorform(instance = request.user,initial={'country':'IN'})
        form2 = UserAddedbyIndividualDoctorform_record(instance = a,initial={'clinic_country':'IN'})
        form3=dict(special_id=aa[0]['special_id'])
        if typeofdoc[0]=='Junior Doctor':
            return render(request,'Created_Individual_Doctor.html', {'form1':form1, 'form2': form2,'form3':form3})
        else:
            return render(request,'Created_Individual_Doctor_Front.html', {'form1':form1, 'form2': form2,'form3':form3})


@csrf_exempt
def individual_doctor_user_list(request):
    user_list=Individual_Doctor_User.objects.filter(user=request.user).values_list('emails',flat=True)
    if (len(user_list)>0):
        from django.db.models import Q
        my_filter_qs = Q()
        for creator in user_list:
            my_filter_qs = my_filter_qs | Q(email=creator)
        user_custom_data=CustomUser.objects.filter(my_filter_qs)
        html = render_to_string('User_List.html', {'user_data': user_custom_data,"page_act":"active" ,"id":"success"})
        return HttpResponse(html)
    else:
        return render(request,'User_List.html')
    
    
@csrf_exempt
def account_status_change(request):
    status=request.GET
    user_list=CustomUser.objects.filter(special_id=status['id']).values_list('is_active',flat=True)
    if user_list[0]==True:
        user_list=CustomUser.objects.filter(special_id=status['id']).update(is_active=False)
        statuss="Inactive"
    else:
        user_list=CustomUser.objects.filter(special_id=status['id']).update(is_active=True)
        statuss="Active"
    return HttpResponse(json.dumps({statuss:statuss}),content_type="application/json")

@hdc_individual_required
@csrf_exempt
def individual_doctor_change_password(request):
    form = PasswordForm()
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            data_json = {"error" : True, "errorMessage" : "Password Mismatch"}
            return JsonResponse(data_json, safe=False)
        else:
            if user.check_password(old_password):
                data1 = CustomUser.objects.get(id=user.id)
                data1.password = make_password(password)
                data1.save()
                data_json = {"error" : False, "errorMessage" : "Password Changed Successfully."}
            else:
                data_json = {"error" : True, "errorMessage" : "Incorrect Old Password"}
            return JsonResponse(data_json, safe=False)
    return render(request, "Individual_Doctor_Change_Password.html", {"form": form})

@csrf_exempt
def set_password(request):
    next = request.GET.get("next")
    form = UserLoginForm(request.POST or None)
    form1 = PasswordUserForm()
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        if not user:
            return redirect('/login_user', messages.error(request, 'Username or password is incorrect', 'alert-danger'))
        else:
            if user.last_login != None:
                login(request, user)
                if next:
                    return redirect(next)
                if request.user.useraddebyindvidualdoctor:
                    return redirect('useraddebyindvidualdoctor')
                return render(request, "Set_Password.html", {'form': form, 'sucessful_submit': False})
            else:          
                login(request, user)  
                return render(request, "Set_Password.html", {'form': form,'form1':form1, 'sucessful_submit': True})
    return render(request, "Set_Password.html", {'form': form,'form1':form1})

@csrf_exempt
def user_password(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password != password_confirm:
            data_json = {"error" : True, "errorMessage" : "Password Mismatch"}
            return JsonResponse(data_json, safe=False)
        else:
            data1 = CustomUser.objects.get(id=user.id)
            data1.password = make_password(password)
            data1.save()
            data_json = {"error" : False, "errorMessage" : "Password Changed Successfully"}
            return JsonResponse(data_json, safe=False)



