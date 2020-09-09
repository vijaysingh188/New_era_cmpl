from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.conf import settings

from accounts.views import (home,password_reset_user_for_event, password_reset_admin, change_password_admin, send_otp_admin, laboratory_edit, 
laboratory_update, laboratory_insertion, verify_otp_admin, login_view_admin, login_view, logout_view, 
contact, activate_account, register, password_reset, contact_master, change_password, send_otp, 
verify_otp, existing_module_master, create_module_master, edit_module_master, destroy_module_master,event_user_tracking,chairpersonlogin,
addservice,addonservice,destroyonservice,pharmacy,pharmacytable,laboratory,lob,destroypharamcy, aboutus, streaming,logout_event,
destroylaboratory,edit_service,edit_pharmacy, add_individual_user, User_creation, account_status_change, Add_streaming_link, user_login, event_register_form, show_events,
coupon_code_list, register1, Coupon_to_create,add_coupon,Coupon_status_change,custom_account_status_change, Custom_user_list, event_visibility,partner_and_event_register,home_event,registerlink,partner_visibility,eventregister,eventtable,editevent,destroyevent,show_questions,jointevent)#,que_sub
from profiles.views import individual_doctor, individual_user, nursing_home, hospital, useraddebyindvidualdoctor, individual_doctor_user_list, individual_doctor_user_creation, individual_doctor_change_password, set_password, user_password
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name="home"),
    path('contact/',contact, name="contact"),
    path('aboutus/',aboutus, name="aboutus"),
    path('register/',register, name="register"),
    path('contact_master/',contact_master, name="contact_master"),
    path('existing_module_master/',existing_module_master, name="existing_module_master"),
    path('create_module_master/',create_module_master, name="create_module_master"),
    path('edit_module_master/<int:module_id>',edit_module_master, name="edit_module_master"),
    path('destroy_module_master/<int:module_id>',destroy_module_master, name="destroy_module_master"),
    path('password_reset/',password_reset, name="password_reset"),
    path('password_reset_admin/',password_reset_admin, name="password_reset_admin"),
    path('change_password/',change_password, name="change_password"),
    path('change_password_admin/',change_password_admin, name="change_password_admin"),
    path('accounts/login/',login_view_admin, name="login_view_admin"),
    path('accounts/login_superadmin/',login_view, name="login_view"),
    path('accounts/logout/',logout_view, name="logout_view"),
    path('send_otp/',send_otp, name="send_otp"),
    path('send_otp_admin/',send_otp_admin, name="send_otp_admin"),
    path('verify_otp/',verify_otp, name="verify_otp"),
    path('verify_otp_admin/',verify_otp_admin, name="verify_otp_admin"),
    path('addservice/',addservice,name="addservice"),
    path('addonservice/',addonservice,name="addonservice"),
    path('destroyonservice/<int:module_id>',destroyonservice,name="destroyonservice"),
    path('pharmacy/',pharmacy,name="pharmacy"),
    path('pharmacytable/',pharmacytable,name="pharmacytable"),
    path('laboratory/',laboratory,name="laboratory"),
    path('laboratory_edit/<int:module_id>',laboratory_edit,name="laboratory_edit"),
    path('laboratory_insertion/',laboratory_insertion,name="laboratory_insertion"), #thru ajax
    path('laboratory_update/',laboratory_update,name="laboratory_update"), #thru ajax
    path('laboratorytable/',lob,name="laboratorytable"),
    path('destroypharamcy/<int:module_id>',destroypharamcy,name="destroypharamcy"),
    path('destroylaboratory/<int:module_id>',destroylaboratory,name="destroylaboratory"),
    path('edit_pharmacy/<int:module_id>',edit_pharmacy, name="edit_pharmacy"),
    path('edit_service/<int:module_id>',edit_service, name="edit_service"),

    path('profile_individual_doctor/',individual_doctor, name="profile_individual_doctor"),
    path('profile_individual_user/',individual_user, name="profile_individual_user"),
    path('profile_hospital/',hospital, name="profile_hospital"),
    path('profile_nursing_home/',nursing_home, name="profile_nursing_home"),

    path('add_individual_user/',add_individual_user,name='add_individual_user'),
    path('User_creation/',User_creation,name='User_creation'),
    path('useraddebyindvidualdoctor/',useraddebyindvidualdoctor, name="useraddebyindvidualdoctor"),
    path('profile_individual_doctor/individual_doctor_user_creation/',individual_doctor_user_creation,name="individual_doctor_user_creation"),
    path('individual_doctor_user_list/',individual_doctor_user_list,name='individual_doctor_user_list'),

    path('account_status_change/',account_status_change,name='account_status_change'),
    path('register1/',register1, name="register1"),

    path('individual_doctor_change_password/',individual_doctor_change_password, name="individual_doctor_change_password"),
    path('login_user/',set_password, name="set_password"),
    path('user_password/',user_password, name="user_password"), #thru ajax

    path('coupon_code_list',coupon_code_list,name='coupon_code_list'),
    path('add_coupon/',add_coupon,name='add_coupon'),
    path('Coupon_to_create',Coupon_to_create,name='Coupon_to_create'),
    path('Coupon_status_change/',Coupon_status_change,name='Coupon_status_change'),
    path('Custom_user_list/', Custom_user_list, name='Custom_user_list'),
    path('custom_account_status_change/',custom_account_status_change,name='custom_account_status_change'),
    
    path('editevent/<int:module_id>',editevent, name="editevent"),
    path('destroyevent/<int:module_id>',destroyevent,name="destroyevent"),
    path('partner_visibility/',partner_visibility,name='partner_visibility'),
    path('eventregister/',eventregister,name="eventregister"),
    path('eventtable/',eventtable,name="eventtable"),
    path('registerlink/<int:module_id>',registerlink,name="registerlink"),
    path('event_visibility/',event_visibility,name="event_visibility"),
    path('home_event',home_event, name="home_event"),
    path('partner_and_event_register/',partner_and_event_register,name="partner_and_event_register"),
    path('Add_streaming_link',Add_streaming_link, name="Add_streaming_link"),
    path('user_login/',user_login, name="user_login"),

    path('event_register_form/<int:module_id>/',event_register_form, name="event_register_form"),
    path('show_events/',show_events, name="show_events"),
    path('password_reset_user_for_event/',password_reset_user_for_event, name="password_reset_user_for_event"),
    path('streaming/<int:id>',streaming,name='streaming'),
    path('jointevent/<int:module_id>',jointevent, name="jointevent"),

    path('show_questions/<int:id>',show_questions,name="show_questions"),
    # path('show_questions/',show_questions,name="show_questions"),

    path('event_user_tracking/',event_user_tracking,name='event_user_tracking'),
    path('logout/',logout_event, name="logout_event"),
    path('chairpersonlogin/',chairpersonlogin,name='chairpersonlogin'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
