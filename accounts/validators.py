from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re

    
from django.core.exceptions import ValidationError
import re



def validate_password_digit(value):
    if not re.search(r"[\d]+", value):
        raise ValidationError("The password must contain at least one digit")
    return value

def validate_password_uppercase(value):
    if not re.search(r"[A-Z]+", value):
        raise ValidationError("The password must contain at least one uppercase character")
    return value
def validate_pass(value):
        if re.search(r"[^A-Za-z0-9]", value) is None:
            raise ValidationError("Missing Symbol")
        return value
