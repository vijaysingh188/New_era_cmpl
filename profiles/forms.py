from django import forms
from django.forms import ModelForm
from accounts.models import CustomUser
from django.forms import inlineformset_factory
from django_countries.fields import CountryField
from .models import UserAddedbyIndividualDoctor	
from django.core.validators import MinLengthValidator
from django.conf import settings

class UserForm(forms.ModelForm):
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
		
	title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Title'}))
	first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
	middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Middle Name'}))
	last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	type_of_doctor = forms.ChoiceField(required=False, choices=doctor_options)
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	house_no = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'House No'}))
	street = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Street'}))
	area = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	city = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	taluka = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	district = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'District'}))
	state = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'State'}))
	pincode = forms.CharField(max_length=6, validators=[MinLengthValidator(6)], widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	country = CountryField(default='IN').formfield()
	name_of_hospital = forms.CharField(required=False)
	owner_name = forms.CharField(required=False)
	no_of_doctor_accounts = forms.CharField(required=False)
	name_of_nursing_home = forms.CharField(required=False)

	class Meta:
		model = CustomUser
		fields = ['title','first_name','middle_name','last_name','type_of_doctor','payment','usecode','phone_no','email','house_no','street','area','city','taluka','district','state','pincode','country','name_of_hospital','no_of_doctor_accounts','owner_name','name_of_nursing_home']

class IndivdualDoctorProfileForm(forms.ModelForm):
	gender_options = (
		('Select Gender', 'Select Gender'),
		('M', 'Male'),
		('F', 'Female'),
		)

	gender = forms.ChoiceField(choices=gender_options)
	dob = forms.DateField(widget=forms.DateInput(attrs={'id':'datetime'}))
	qualification = forms.CharField()
	speciality1 = forms.CharField()
	speciality2 = forms.CharField(required=False)
	speciality3 = forms.CharField(required=False)
	practicing_since = forms.CharField()
	reg_no_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	reg_no_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Number'}))
	reg_no_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Year'}))
	picture = forms.ImageField(widget=forms.FileInput,required=False)
	phone_no1 = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email1 = forms.CharField(max_length=150, required=False,error_messages={'required':'Enter a Valid Email Address'})
	landline_no = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	landline_no1 = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	res_house_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'House No'}))
	res_street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
	res_area = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	res_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	res_taluka = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	res_district = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'District'}))
	res_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	res_pincode = forms.CharField(max_length=6, validators=[MinLengthValidator(6)], widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	res_country = CountryField(default='IN').formfield()


	class Meta:
		model = CustomUser
		fields = ['gender','dob','qualification','speciality1','speciality2','speciality3','practicing_since','reg_no_state','reg_no_number','reg_no_year','email1','picture','phone_no1','landline_no','landline_no1','res_state','res_country','res_pincode','res_district','res_street','res_area','res_taluka','res_house_no','res_city']

class NursingHomeProfileForm(forms.ModelForm):
	speciality1 = forms.CharField()
	speciality2 = forms.CharField(required=False)
	speciality3 = forms.CharField(required=False)
	reg_no_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	reg_no_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Number'}))
	reg_no_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Year'}))
	picture = forms.ImageField(widget=forms.FileInput,required=False)
	phone_no1 = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email1 = forms.CharField(max_length=150, required=False,error_messages={'required':'Enter a Valid Email Address'})
	landline_no = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})

	class Meta:
		model = CustomUser
		fields = ['speciality1','speciality2','speciality3','reg_no_state','reg_no_number','reg_no_year','email1','picture','phone_no1','landline_no']

class HospitalProfileForm(forms.ModelForm):
	speciality1 = forms.CharField()
	speciality2 = forms.CharField(required=False)
	speciality3 = forms.CharField(required=False)
	reg_no_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
	reg_no_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Number'}))
	reg_no_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Year'}))
	picture = forms.ImageField(widget=forms.FileInput)
	phone_no1 = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email1 = forms.CharField(max_length=150, required=False,error_messages={'required':'Enter a Valid Email Address'})
	landline_no = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})

	class Meta:
		model = CustomUser
		fields = ['speciality1','speciality2','speciality3','reg_no_state','reg_no_number','reg_no_year','email1','picture','phone_no1','landline_no']

class IndivdualUserProfileForm(forms.ModelForm):
	gender_options = (
		('Select Gender', 'Select Gender'),
		('Male', 'Male'),
		('Female', 'Female'),
		)
	relationship_options = (
		('Select Relationship', 'Select Relationship'),
		('Mother', 'Mother'),
		('Father', 'Father'),
		('Daughter', 'Daughter'),
		('Son', 'Son'),
		('Wife', 'Wife'),
		('Husband', 'Husband'),
		('Brother', 'Brother'),
		('Sister', 'Sister'),
		)

	gender = forms.ChoiceField(choices=gender_options)
	dob = forms.DateField(widget=forms.DateInput(attrs={'id':'datetime'}),required=False)
	phone_no1 = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	email1 = forms.CharField(max_length=150, required=False,error_messages={'required':'Enter a Valid Email Address'})
	landline_no = forms.CharField(required=False,max_length=10, validators=[MinLengthValidator(10)],error_messages={'required':'Enter a Valid Phone Number'})
	relationship = forms.ChoiceField(choices=relationship_options)
	relation_name = forms.CharField()
	relation_phone_no = forms.CharField(required=False)
	relation_email = forms.CharField(max_length=150, required=False,error_messages={'required':'Enter a Valid Email Address'})

	class Meta:
		model = CustomUser
		fields = ['gender','dob','phone_no1','email1','landline_no','relationship','relation_name','relation_phone_no','relation_email']


class UserAddedbyIndividualDoctorform(forms.ModelForm):
	Type_of_doctor = (
		('DF','Junior Doctor'),
        ('DG','Front Desk')
        )
	Title = (
		('Mr.', 'Mr.'),
		('Ms.', 'Ms.'),
		('Mrs.', 'Mrs.'),
		('Dr.', 'Dr.'),
		)
	type_of_doctor=forms.ChoiceField(required=False,choices=Type_of_doctor)
	title=forms.ChoiceField(required=True,choices=Title)
	first_name = forms.CharField(max_length=150)
	middle_name = forms.CharField(max_length=150)
	last_name = forms.CharField(max_length=150)
	phone_no = forms.CharField(max_length=150)
	email = forms.CharField(max_length=150)
	payment = forms.CharField(required=False)
	usecode = forms.CharField(required=False)
	house_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'House No'}))
	street = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Street'}))
	area = forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
	city = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
	taluka = forms.CharField(required=False,  widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
	district = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'District'}))
	state = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'State'}))
	pincode = forms.CharField( required=False, widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
	country = CountryField().formfield(required=False)
	name_of_hospital = forms.CharField(required=False)
	owner_name = forms.CharField(required=False)
	no_of_doctor_accounts = forms.CharField(required=False)
	name_of_nursing_home = forms.CharField(required=False)

	class Meta:
		model = CustomUser
		fields = ['title','first_name','middle_name','last_name','type_of_doctor','payment','usecode','phone_no','email','house_no','street','area','city','taluka','district','state','pincode','country','name_of_hospital','no_of_doctor_accounts','owner_name','name_of_nursing_home']

class UserAddedbyIndividualDoctorform_record(forms.ModelForm):
    Title = (
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Mrs.', 'Mrs.'),
        ('Dr.', 'Dr.'),
        )
    gender_options = (
        ('Select Gender', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        )

    Speciality_options = (
        ('Speciality', 'Speciality'),
        ('Speciality1', 'Speciality1'),
        ('Speciality2', 'Speciality2'),
        ('Speciality3', 'Speciality3'),
        )
    type_of_doctor=forms.CharField(required=False)
    house_no = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'House No'}))
    street = forms.CharField( required=False,widget=forms.TextInput(attrs={'placeholder':'Street'}))
    area = forms.CharField( required=False,widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
    taluka = forms.CharField( required=False,widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
    district = forms.CharField( required=False,widget=forms.TextInput(attrs={'placeholder':'District'}))
    state = forms.CharField( required=False,widget=forms.TextInput(attrs={'placeholder':'State'}))
    pincode = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
    country =  CountryField(default='IN').formfield()
    dob =forms.DateField(widget=forms.DateInput(attrs={'id':'datetime_from1','autocomplete': 'off','placeholder':'DoB'},format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)
    picture = forms.ImageField(required=False,widget=forms.FileInput)
    gender = forms.ChoiceField(required=True,choices=gender_options)
    qualification = forms.CharField(required=True,max_length=150)
    age = forms.CharField(required=False,widget=forms.TextInput(attrs={'id':'age'}))
    speciality1 = forms.CharField()
    speciality2 = forms.CharField(required=False)
    speciality3 = forms.CharField(required=False)
    reg_no_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
    reg_no_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Year'}))
    practicing_since = forms.CharField(required=False,max_length=150)
    pictureof_certificate = forms.ImageField(widget=forms.FileInput,required=False)
    phone_no2 = forms.CharField(required=False,max_length=150)
    email2 = forms.EmailField(required=False)
    reg_no_number = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'Number'}))
    clinic_house_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'House No'}))
    clinic_street = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Street'}))
    clinic_area = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Locality / Area / Pada'}))
    clinic_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'City / Town / Village'}))
    clinic_taluka = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Taluka'}))
    clinic_district = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'District'}))
    clinic_state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State'}))
    clinic_pincode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Pin Code'}))
    clinic_landline = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landline NO'}))
    clinic_country = CountryField(default='IN').formfield()

    class Meta:
        model = CustomUser
        fields = ['type_of_doctor','house_no','dob','street','country','clinic_country','area','city','taluka','district','state','pincode','picture','gender','qualification','age','speciality1','practicing_since', 'reg_no_year','reg_no_state','speciality2','speciality3', 'pictureof_certificate','phone_no2','email2','reg_no_number','clinic_house_no','clinic_street','clinic_area','clinic_city','clinic_taluka','clinic_district','clinic_state','clinic_pincode','clinic_landline']

		
class PasswordForm(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInput1','placeholder':'Old Password'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInput2','placeholder':'New Password'}))
	password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInput3','placeholder':'Re-enter Password'}))
		
class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Phone Number/Email-id'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInput','placeholder':'Enter Password'}))
		
class PasswordUserForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInputpop1','placeholder':'New Password'}))
	password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'id':'myInputpop2','placeholder':'Re-enter Password'}))

		
