from django.contrib.auth import login, logout, user_logged_in, user_logged_out
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

def encode_uid(pk):
    return force_text(urlsafe_base64_encode(force_bytes(pk)))

def decode_uid(pk):
    return force_text(urlsafe_base64_decode(pk))

def get_user_email(user):
    email_field_name = get_user_email_field_name(user)
    return getattr(user, email_field_name, None)

def get_user_email_field_name(user):
    return user.get_email_field_name()
