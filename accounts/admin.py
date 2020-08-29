from django.contrib import admin
from accounts.models import Eventregisterationuser,Webregister,CustomUser

# Register your models here.
class Eventregisteradmin(admin.ModelAdmin):
    list_filter = ['id']


admin.site.register(Eventregisterationuser,Eventregisteradmin)

class WebregisterAdmin(admin.ModelAdmin):
    list_display = ['eventtitle','id','organizedby']
    list_filter = ['id']
admin.site.register(Webregister,WebregisterAdmin)

admin.site.register(CustomUser)