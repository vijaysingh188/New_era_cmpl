from django.contrib.auth.backends import ModelBackend
from accounts.models import CustomUser

class SODMZSModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwars):
        # the username could be either one of the two
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'phone_no': username}
        try:
            user = CustomUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return CustomUser.objects.get(pk=username)
        except CustomUser.DoesNotExist:
            return None