from django.db import models
from django.contrib.auth.models import AbstractUser
# from jsonfield import JSONField
# from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields.jsonb import JSONField
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import requests
from django_countries.fields import CountryField
from django.db import models
import jsonfield

df = []


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    firstname = models.CharField(max_length=10, blank=True, null=True)
    middlename = models.CharField(max_length=10, blank=True, null=True)
    lastname = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=10, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(max_length=255, unique=True, null=True, blank=True)
    payment = models.CharField(max_length=255, blank=True, null=True)
    usecode = models.CharField(max_length=255, blank=True, null=True)
    type_of_doctor = models.CharField(max_length=255, blank=True, null=True)
    name_of_hospital = models.CharField(max_length=255, blank=True, null=True)
    house_no = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    taluka = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=255, blank=True, null=True)
    country = CountryField(default='IN')
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    no_of_doctor_accounts = models.CharField(max_length=255, blank=True, null=True)
    name_of_nursing_home = models.CharField(max_length=255, blank=True, null=True)
    is_individual = models.BooleanField(default=False)
    is_hdc_individual = models.BooleanField(default=False)
    is_hdc_hospital = models.BooleanField(default=False)
    is_hdc_nursing_home = models.BooleanField(default=False)
    useraddebyindvidualdoctor=models.BooleanField(default=False)
    special_id = models.CharField(max_length=255, null=True, default=None)
    register_link = jsonfield.JSONField(default=df, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self,*args, **kwargs):
        if not self.special_id:
            if self.type_of_doctor == "DA":
                prefix = 'DA{}'.format(timezone.now().strftime('%y%m%d'))
            elif self.type_of_doctor == "DB":
                prefix = 'DB{}'.format(timezone.now().strftime('%y%m%d'))
            elif self.type_of_doctor == "DC":
                prefix = 'DC{}'.format(timezone.now().strftime('%y%m%d'))
            elif self.type_of_doctor == "DD":
                prefix = 'DD{}'.format(timezone.now().strftime('%y%m%d'))
            elif self.type_of_doctor == "DE":
                prefix = 'DE{}'.format(timezone.now().strftime('%y%m%d'))
            elif self.type_of_doctor == "DF":
                prefix = 'DF{}'.format(timezone.now().strftime('%y%m%d'))
            elif self.type_of_doctor == "DG":
                prefix = 'DG{}'.format(timezone.now().strftime('%y%m%d'))
            else:
                prefix = 'AA{}'.format(timezone.now().strftime('%y%m%d'))
            prev_instances = self.__class__.objects.filter(special_id__contains=prefix)
            if prev_instances.exists():
                last_instance_id = prev_instances.last().special_id[-4:]
                self.special_id = prefix+'{0:04d}'.format(int(last_instance_id)+1)
            else:
                self.special_id = prefix+'{0:04d}'.format(1)
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class SecurityQuestions(models.Model):
    question = models.CharField(max_length=255, blank=True)
    answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.question

class ModuleMaster(models.Model):
    module_name = models.CharField(max_length=255, blank=True)
    module_code = models.CharField(max_length=255, blank=True)
    no_of_patients = models.IntegerField(default = 0)
    web_space = models.IntegerField(default = 0)
    amount = models.IntegerField(default = 0)
    cgst = models.IntegerField(default = 0)
    sgst = models.IntegerField(default = 0)
    gst = models.IntegerField(default = 0)
    total_amount = models.IntegerField(default = 0)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.module_name

class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True)
    phone_no = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    message = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class AddOnServices(models.Model):
    add_onservices = models.CharField(max_length=255)
    add_on_servicescode = models.CharField(max_length=255)
    amount = models.FloatField(default = 0)
    cgst = models.FloatField(default = 0)
    sgst = models.FloatField(default = 0)
    gst = models.FloatField(default = 0)
    total_amount = models.FloatField(default = 0)

    def __str__(self):
        return self.add_onservices

class pharamcytab(models.Model):
    companyname = models.CharField(max_length=255)
    addresslineone=models.CharField(max_length=255)
    addresslinetwo = models.CharField(max_length=255)
    streetname = models.CharField(max_length=255)
    city= models.CharField(max_length=255)
    country= CountryField(default='IN')
    state= models.CharField(max_length=255)
    pincode= models.IntegerField(default = 0)
    nationalhead= models.CharField(max_length=266)
    contactnumber= models.CharField(max_length=255, blank=True)
    emailaddress= models.EmailField()
    phonenumber= models.CharField(max_length=255, blank=True)
    regionalhead= models.CharField(max_length=255)
    regionalcontactnumber= models.CharField(max_length=255, blank=True)
    regionalemailaddress= models.CharField(max_length=255)
    regionalphonenumber= models.CharField(max_length=255, blank=True)
    scientifichead=models.CharField(max_length=266)
    scientificcontactnumber= models.CharField(max_length=255, blank=True)
    scientificemailaddress= models.EmailField()
    scientificphonenumber=models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.city

class LaboratoryModule(models.Model):
    investigation_name = models.CharField(max_length=255, blank=True)
    synonyms = models.CharField(max_length=255, blank=True)
    important_note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.investigation_name)

class LaboratoryPreDefine(models.Model):
    investigation =models.ForeignKey('LaboratoryModule',on_delete=models.CASCADE)
    select_dropdown_list = models.CharField(max_length=150)
    select = models.CharField(max_length=150)

    def __str__(self):
        return str(self.investigation_id)

class LaboratoryEmpty(models.Model):
    investigation =models.ForeignKey('LaboratoryModule',on_delete=models.CASCADE)
    from_age = models.CharField(max_length=255, blank=True)
    to_age = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    conventional = models.CharField(max_length=255, blank=True)
    umo1 = models.CharField(max_length=255, blank=True)
    umo2 = models.CharField(max_length=255, blank=True)
    conversion_factor = models.CharField(max_length=255, blank=True)
    high1 = models.CharField(max_length=255, blank=True)
    low1 = models.CharField(max_length=255, blank=True)
    high2 = models.CharField(max_length=255, blank=True)
    low2 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.investigation_id)

class CouponManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('code')

    def expired(self):
        return self.filter(endDate__lt=timezone.now())

class Coupon(models.Model):
    PROFILE_CHOICES = (
        ('is_individual', 'is_individual'),
        ('is_hdc_individual', 'is_hdc_individual'),
        ('is_hdc_hospital', 'is_hdc_hospital'),
        ('is_hdc_nursing_home', 'is_hdc_nursing_home')

    )
    code = models.CharField(max_length=6)
    startDate = models.DateField()
    endDate = models.DateField()
    count_value = models.IntegerField(default=100)
    profileChoices = models.CharField(choices=PROFILE_CHOICES, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    coupon = CouponManager()

    def expired(self):
        return self.endDate is not None and self.endDate < timezone.now()

    def __str__(self):
        return self.code


class Webregister(models.Model):
    eventtitle = models.CharField(max_length=255)
    targetaudiance = models.CharField(max_length=255)
    eventtype = models.CharField(max_length=255)
    created_on = models.DateTimeField(null=True, blank=True)
    ends_on = models.DateTimeField(null=True, blank=True)
    Chairpersons = models.CharField(max_length=255)
    mobilenumber = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    Moderatorname = models.CharField(max_length=266)
    mmobile = models.CharField(max_length=255, blank=True)
    memail = models.EmailField()
    ContactPersonanme = models.CharField(max_length=255, blank=True)
    Cmobile = models.CharField(max_length=255)
    Cemail = models.EmailField()
    organizedby = models.CharField(max_length=255)
    sponserby = models.CharField(max_length=255, blank=True)
    Registerationrequired = models.CharField(max_length=266)
    paymentrequired = models.CharField(max_length=255, blank=True)
    partnerrequired = models.CharField(max_length=255)
    creation_link = models.URLField(max_length=255,null=True,blank=True)
    register_link = models.CharField(max_length=255,null=True,blank=True)
    streaming_link = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return str(self.pk)
        
    class Meta:
        ordering = ['-created_on']

class Eventregisterationuser(models.Model):
    webregister = models.ForeignKey(Webregister,on_delete=models.CASCADE)
    header_eventimage = models.FileField(upload_to='images',null=True, blank=True)
    footer_eventimage = models.FileField(upload_to='images',null=True, blank=True)
    streaming_header = models.FileField(upload_to='images',null=True, blank=True)
    streaming_leftpanel = models.FileField(upload_to='images',null=True, blank=True)
    streaming_rightpanel = models.FileField(upload_to='images',null=True, blank=True)
    ticker_content = models.CharField(null=True, blank=True,max_length=255)
    ticker_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class Question(models.Model):
    webregister = models.ForeignKey(Webregister, on_delete=models.CASCADE)
    que = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return str(self.pk)
    # class Meta:
    #     ordering = ['-que']


class Rlink(models.Model):
    customUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    webregister = models.ForeignKey(Webregister, on_delete=models.CASCADE)
    register_link = models.CharField(max_length=255,null=True, blank=True)
    def __str__(self):
        return str(self.pk)






