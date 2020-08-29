from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms import ModelForm
from .models import SecurityQuestions, ModuleMaster, Contact, CustomUser, AddOnServices, pharamcytab, Coupon, LaboratoryModule,Webregister,Eventregisterationuser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django_countries.fields import CountryField
from accounts.validators import validate_password_digit, validate_password_uppercase,validate_pass
from django.conf import settings
#from accounts.validators import validate_password_digit, validate_password_uppercase,validate_pass

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ('email',)


class IndivdualUserForm(ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}),required=False)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Middle Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	phone_no = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email = forms.EmailField(required=False,error_messages={'required':'Enter a Valid Email Address'})
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInput1','placeholder':'Create Password'}),required=False)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2','placeholder':'Confrim Password'}), required=False)
	usecode = forms.CharField(required=False)
	class Meta:
		model = CustomUser
		fields = ['title','first_name','middle_name','last_name','phone_no','email','password','usecode']



class IndivdualDoctorForm(ModelForm):
	doctor_options = (
		('Select Type','Select Type'),
		('DA','Allopathy'),
		('DB','Ayurveda'),
		('DC','Homoeopathy'),
		('DD','Unani'),
		('DE','Siddha'),
		('DF','Junior Doctor'),
		('DG','Front Desk'),
		)
	type_of_doctor = forms.ChoiceField(choices=doctor_options)
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}),required=False)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Middle Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	phone_no = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	email = forms.EmailField(required=False,error_messages={'required':'Enter a Valid Email Address'})
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInput2','placeholder':'Create Password'}),required=False)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2','placeholder':'Confirm Password'}), required=False)
	class Meta:
		model = CustomUser
		fields = ['type_of_doctor','title','first_name','middle_name','last_name','phone_no','payment','usecode','email','password']


class HospitalForm(ModelForm):
	name_of_hospital = forms.CharField()
	house_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'House No'}))
	street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
	area = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	taluka = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	district = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'District'}))
	state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	pincode = forms.CharField(max_length=6, validators=[MinLengthValidator(6)], widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	country = CountryField(default='NZ').formfield()
	owner_name = forms.CharField()
	phone_no = forms.CharField(required=False, validators=[MinLengthValidator(10)], max_length=10,error_messages={'required':'Enter a Valid Phone Number'})
	email = forms.EmailField(required=False,error_messages={'required':'Enter a Valid Email Address'})
	no_of_doctor_accounts = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'pass'}),required=False)
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	class Meta:
		model = CustomUser
		fields = ['payment','usecode','name_of_hospital','house_no','street','area','city','taluka','district','state','pincode','country','owner_name','phone_no','email','no_of_doctor_accounts','password']

class NursingHomeForm(ModelForm):
	name_of_nursing_home = forms.CharField()
	house_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'House No'}))
	street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
	area = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	taluka = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	district = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'District'}))
	state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	pincode = forms.CharField(max_length=6, validators=[MinLengthValidator(6)], widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	country = CountryField(default='IN').formfield()
	owner_name = forms.CharField()
	phone_no = forms.CharField(required=False,max_length=10,validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email = forms.EmailField(required=False,error_messages={'required':'Enter a Valid Email Address'})
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	no_of_doctor_accounts = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'pwword'}),required=False)
	class Meta:
		model = CustomUser
		fields = ['payment','usecode','name_of_nursing_home','house_no','street','area','city','taluka','district','state','pincode','country','owner_name','phone_no','email','no_of_doctor_accounts','password']


class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email / Phone No.'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))


class SecurityQuestionsForm(ModelForm):
	question = forms.CharField(label='question', widget=forms.TextInput(attrs={'placeholder':'Security Question'}))
	answer = forms.CharField(label='answer', widget=forms.TextInput(attrs={'placeholder':'Answer'}))
	class Meta:
		model = SecurityQuestions
		fields = ['question','answer']

class PasswordForm(forms.Form):
	password = forms.CharField(disabled=True, widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
	password_confirm = forms.CharField(disabled=True, widget=forms.PasswordInput(attrs={'placeholder':'Re-enter Password'}))

class PasswordVerificationAdminForm(forms.Form):
	email = forms.CharField(disabled=False, label='email', widget=forms.TextInput(attrs={'placeholder':'Registered Email','id': 'email'}))
	phone_no = forms.CharField(disabled=True,label='phone_no', widget=forms.TextInput(attrs={'placeholder':'Enter OTP','id': 'otptxt'}))


class PasswordVerificationForm(forms.Form):
	question = forms.ModelChoiceField(disabled=True, queryset=SecurityQuestions.objects.all(), empty_label=None, widget=forms.Select(attrs={'class':'form-control','id': 'sectxt'}))
	answer = forms.CharField(disabled=True, label='answer', widget=forms.TextInput(attrs={'placeholder':'Answer','id': 'anstxt'}))
	phone_no = forms.CharField(disabled=True,label='phone_no', widget=forms.TextInput(attrs={'placeholder':'Enter OTP','id': 'otptxt'}))

class ModuleMasterForm(ModelForm):
	module_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Module Name'}))
	module_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Module Code'}))
	no_of_patients = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Number of Patients'}))
	web_space = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mb'}))
	amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'in Rupees','id':'amount'}))
	cgst = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'%', 'id':'cgst'}))
	sgst = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'%', 'id':'sgst'}))
	gst = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'%','id':'gst','onfocus':'sum()'}))
	total_amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'in Rupees','id':'tot_amount','onfocus':'sum1()'}))

	class Meta:
		model = ModuleMaster
		fields = ['module_name','module_code','no_of_patients','web_space','amount','cgst','sgst','gst','total_amount']


class ContactForm(ModelForm):
	name = forms.CharField()
	phone_no = forms.CharField(required=False,max_length=10,validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email = forms.CharField(required=False,error_messages={'required':'Enter a Valid Email Address'})
	message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 5}))

	class Meta:
		model = Contact
		fields = ['name','phone_no','email','message']

class AddServices(ModelForm):
	add_onservices = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add_on service'}),required=False)
	add_on_servicescode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add-on Services Code'}),required=False)
	amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'amount','id':'amount'}),required=False)
	cgst = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'%','id':'cgst'}),required=False)
	sgst = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'%','id':'sgst'}),required=False)
	gst = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'%','id':'gst','onfocus':'sum()'}),required=False)
	total_amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'in Rupees','id':'tot_amount','onfocus':'sum1()'}),required=False)

	class Meta:
		model = AddOnServices
		fields = ['add_onservices','add_on_servicescode','amount','cgst','sgst','gst','total_amount']


class pharamcy(ModelForm):
   companyname=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'name'}))
   addresslineone=forms.CharField(required=False)
   addresslinetwo = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'address'}),required=False)
   streetname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'streetname'}),required=False)
   city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'city'}),required=False)
   country = CountryField()
   state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'state'}),required=False)
   pincode = forms.CharField(max_length=6,validators=[MinLengthValidator(6)],widget=forms.TextInput(attrs={'placeholder':'pincode'}),required=False)
   nationalhead = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'nationalhead'}),required=False)
   contactnumber = forms.CharField(max_length=10, validators=[MinLengthValidator(10)], required=False)
   emailaddress = forms.EmailField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
   phonenumber = forms.CharField(max_length=10, validators=[MinLengthValidator(10)], required=False)
   regionalhead =forms.CharField(widget=forms.TextInput(attrs= {'placeholder':'head'}),required=False)
   regionalcontactnumber = forms.CharField(max_length=10, validators=[MinLengthValidator(10)], required=False)
   regionalemailaddress = forms.CharField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
   regionalphonenumber = forms.CharField(max_length=10, validators=[MinLengthValidator(10)],required=False)
   scientifichead = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'head'}),required=False)
   scientificcontactnumber = forms.CharField(max_length=10, validators=[MinLengthValidator(10)], required=False)
   scientificemailaddress = forms.EmailField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
   scientificphonenumber = forms.CharField(max_length=10, validators=[MinLengthValidator(10)], required=False)
    
   class Meta:
       model = pharamcytab
       fields = ['companyname','addresslineone','addresslinetwo','streetname','city','country','state','pincode','nationalhead','contactnumber','emailaddress','phonenumber','regionalhead','regionalcontactnumber','regionalemailaddress','regionalphonenumber','scientifichead','scientificcontactnumber','scientificemailaddress','scientificphonenumber']

class IndivdualUserForm1(ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Middle Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	phone_no = forms.CharField(required=False, validators=[MinLengthValidator(10)],max_length=10,error_messages={'required':'Enter a Valid PhoneNumber'})
	email = forms.EmailField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
	password = forms.CharField(widget=forms.PasswordInput())
	usecode = forms.CharField(required=False)
	class Meta:
		model = CustomUser
		fields = ['title','first_name','middle_name','last_name','phone_no','email','password','usecode']
	#def clean(self, *args,**kwargs):
	#	email = self.cleaned_data['email']
	#	if CustomUser.objects.filter(email=email).exists():
	#		raise ValidationError("Email already exists")
	#	return super(IndivdualUserForm, self).clean(*args, **kwargs)


class IndivdualDoctorForm1(ModelForm):
	doctor_options = (
		('Select Type','Select Type'),
		('DA','Allopathy'),
		('DB','Ayurveda'),
		('DC','Homoeopathy'),
		('DD','Unani'),
		('DE','Siddha'),
		('DF','Junior Doctor'),
		('DG','Front Desk'),
		)
	type_of_doctor = forms.ChoiceField(choices=doctor_options)
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Middle Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	phone_no = forms.CharField(required=False, validators=[MinLengthValidator(10)],max_length=10,error_messages={'required':'Enter Valid Phone Number'})
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	email = forms.EmailField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'pwd1'}), validators=[MinLengthValidator(6)])
	class Meta:
		model = CustomUser
		fields = ['type_of_doctor','title','first_name','middle_name','last_name','phone_no','payment','usecode','email','password']


class HospitalForm1(ModelForm):
	name_of_hospital = forms.CharField()
	street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
	area = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	taluka = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	district = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'District'}))
	state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	pincode = forms.CharField(validators=[MinLengthValidator(10)],max_length=6,widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	country =CountryField(default='IN')
	owner_name = forms.CharField()
	phone_no = forms.CharField(required=False)
	email = forms.EmailField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
	no_of_doctor_accounts = forms.CharField()
	password =forms.CharField(widget=forms.PasswordInput(attrs={'id':'password1'}), validators=[MinLengthValidator(6)])
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	class Meta:
		model = CustomUser
		fields = ['payment','usecode','name_of_hospital','street','area','city','taluka','district','state','pincode','country','owner_name','phone_no','email','no_of_doctor_accounts','password']

class NursingHomeForm1(ModelForm):
	name_of_nursing_home = forms.CharField()
	street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
	area = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	taluka = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	district = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'District'}))
	state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	pincode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	country = CountryField(default='IN')
	owner_name = forms.CharField()
	phone_no = forms.CharField(required=False, validators=[MinLengthValidator(10)],max_length=10,error_messages={'required':'Invalid Phone Number'})
	email = forms.EmailField(error_messages={'required':'Enter a Valid Email Address'},widget=forms.TextInput(attrs={'placeholder':'email'}),required=False)
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	no_of_doctor_accounts = forms.CharField()
	password =forms.CharField(widget=forms.PasswordInput(attrs={'id':'pwd'}), validators=[MinLengthValidator(6)])
	class Meta:
		model = CustomUser
		fields = ['payment','usecode','name_of_nursing_home','street','area','city','taluka','district','state','pincode','country','owner_name','phone_no','email','no_of_doctor_accounts','password']



class CouponForm(ModelForm):
	class Meta:
		model = Coupon
		fields = ['code','count_value','startDate','endDate','profileChoices']
		

class EventregisteruserForm(ModelForm):
    use_required_attribute = False
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(EventregisteruserForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['ticker_content'].required = False
        self.fields['ticker_time'].required = False

    # header_eventimage = forms.ImageField(widget=forms.FileInput, required=False)        #,validators=[header_eventimage]
    header_eventimage = forms.FileField(widget=forms.FileInput, required=False)
    footer_eventimage = forms.FileField(widget=forms.FileInput, required=False)
    streaming_header = forms.FileField(widget=forms.FileInput, required=False)
    streaming_rightpanel = forms.FileField(widget=forms.FileInput, required=False)
    streaming_leftpanel = forms.FileField(widget=forms.FileInput, required=False)
    # ticker_content = forms.CharField(widget=forms.TextInput(attrs={'required':'false'}))
    ticker_content = forms.CharField(required=False)
    ticker_time = forms.IntegerField(required=False)
    # ticker_time = forms.IntegerField(widget=forms.NumberInput(attrs={'required':'false'}))

    class Meta:
        model = Eventregisterationuser
        fields = ['header_eventimage','footer_eventimage','streaming_header','streaming_leftpanel','streaming_rightpanel','ticker_content','ticker_time']


class Eventregistertable(forms.ModelForm):
    eventtitle = forms.CharField(widget=forms.TextInput(attrs={'id': 'eventtitle'}))
    TARGET_OPTION = (
        ('Health Delivery Center', 'Health Delivery Center'),
        ('Individual', 'Individual'),
        ('Both', 'Both')
    )
    targetaudiance = forms.ChoiceField(choices=TARGET_OPTION,widget=forms.Select(attrs={'id':'targetaudiance'}))   #targetaudiance choices=TARGET_OPTION

    EVENT_OPTION = (
        ('Webinar', 'webinar'),
        ('Conference', 'Conference'),
    )
    eventtype = forms.ChoiceField(choices=EVENT_OPTION) #format='%Y-%m-%d %H:%M:%S',
    created_on = forms.DateTimeField(widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}))  #format='%Y-%m-%dT%H:%M 12:30PM Sep 2020
    ends_on = forms.DateTimeField(widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}))
    Chairpersons = forms.CharField(widget=forms.TextInput(),required=False)
    mobilenumber = forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(), required=False)
    email = forms.EmailField(required=False)
    Moderatorname = forms.CharField(widget=forms.TextInput(), required=False)
    mmobile = forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(), required=False)
    memail = forms.EmailField(required=False)
    ContactPersonanme = forms.CharField(widget=forms.TextInput(), required=False)
    Cmobile = forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(), required=False)
    Cemail = forms.EmailField(required=False)
    organizedby = forms.CharField(widget=forms.TextInput(), required=False)
    sponserby = forms.CharField(widget=forms.TextInput(), required=False)
    CHOICES = (
        ('Yes', 'Yes'), ('No', 'NO'),
    )
    Registerationrequired = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)

    CHOICES = (
        ('Yes', 'Yes'), ('No', 'NO'),
    )
    paymentrequired = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)
    CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'NO'),
    )

    partnerrequired = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)

    class Meta:
        model = Webregister
        fields = ['eventtitle', 'targetaudiance', 'eventtype', 'created_on','ends_on','Chairpersons','mobilenumber',
                  'email', 'Moderatorname', 'mmobile', 'memail', 'ContactPersonanme', 'Cmobile', 'Cemail',
                  'organizedby','sponserby','Registerationrequired', 'paymentrequired', 'partnerrequired']

class SignUpForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ['firstname','middlename','lastname','email','phone_no']
