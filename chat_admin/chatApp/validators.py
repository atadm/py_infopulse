from django.core.exceptions import ValidationError
import re

# def not_null(data):
#     if data == None:
#         raise ValidationError("This field cannot be null")

def email_validation(data):
    #pattern = re.compile(r'\w{1,}')
    pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
    isemail = pattern.match(data)
    #print("isemail"+str(isemail.group(0)))
    if isemail==None:
        raise ValidationError("Your login is not email")
