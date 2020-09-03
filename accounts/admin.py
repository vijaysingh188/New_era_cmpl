from django.contrib import admin
from accounts.models import Eventregisterationuser,Webregister,CustomUser,Question,Rlink,Coupon

# Register your models here.
class Eventregisteradmin(admin.ModelAdmin):
    list_filter = ['id']


admin.site.register(Eventregisterationuser,Eventregisteradmin)

class WebregisterAdmin(admin.ModelAdmin):
    list_display = ['eventtitle','id','organizedby']
    list_filter = ['id']
admin.site.register(Webregister,WebregisterAdmin)

admin.site.register(CustomUser)
admin.site.register(Question)
admin.site.register(Rlink)
admin.site.register(Coupon)