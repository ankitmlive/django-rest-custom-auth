from rest_framework import serializers
from accounts.models import MyUser
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.utils import decode_uid
from .tokens import account_activation_token

User = get_user_model()

class UserRegistrationSerializer(serializers.Serializer):
    fullname    = serializers.CharField(required=True)
    email       = serializers.EmailField(required=True, label="Email Address")
    username    = serializers.CharField(max_length=200)
    password    = serializers.CharField(required=True, label="Password", style={'input_type': 'password'})
    password_2  = serializers.CharField(required=True, label="Confirm Password", style={'input_type': 'password'})

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError("Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8))
        return value

    def save(self):
        fullname = self.validated_data['fullname']
        username = self.validated_data['username']
        email    = self.validated_data['email']
        password = self.validated_data['password']
        user_obj = User(
                username = username,
                email = email,
                fullname = fullname,
            )
        user_obj.set_password(password)
        user_obj.is_active = False
        user_obj.save()
        return user_obj

class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False, allow_blank=True, write_only=True,)
    email = serializers.EmailField(required=False, allow_blank=True, write_only=True, label="Email Address")
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta(object):
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to login.")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            data["user"] = user_obj
        else:
            raise serializers.ValidationError("User not active.")

        return data

class UserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_token": "invlai token provided",
        "invalid_uid": "invalid uid user",
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # check the user for this uid is available or not in DB
        try:
            uid = decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError( {"uid": [self.error_messages[key_error]]}, code=key_error )
        
        # check the token for this token is available or not in DB
        if user is not None and account_activation_token.check_token(user, token):
            user.profile.email_confirmed = True
            user.save()

        data["user"] = user_obj
        # is_token_valid = self.context["view"].token_generator.check_token(
        #     self.user, self.initial_data.get("token", "")
        # )
        
        # if is_token_valid:
        #     return validated_data
        # else:
        #     key_error = "invalid_token"
        #     raise ValidationError( {"token": [self.error_messages[key_error]]}, code=key_error)



# class UserActivationSerializer(UidAndTokenSerializer):

#     default_error_messages = {
#         "stale_token": "stale token"
#     }

#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#         if not self.user.is_active:
#             return attrs
#         #raise exceptions.PermissionDenied(self.error_messages["stale_token"])
#         raise exceptions.PermissionDenied("permission denied")
   
