from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from accounts.utils import decode_uid
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()

#--> User Serializers
class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email', 'fullname', 'title', 'avatar']
        read_only_fields = ('pk', 'username', 'email',)

#--> checkUsername serializer
class CheckUsernameSerializer(serializers.Serializer):
    username    = serializers.CharField(max_length=50)
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            available = True
        else:
            available = False
        return available

#--> auth serializers
class UserRegistrationSerializer(serializers.Serializer):
    email       = serializers.EmailField(required=True, label="Email Address")
    username    = serializers.CharField(max_length=200)
    password    = serializers.CharField(required=True, label="Password", style={'input_type': 'password'})
    confirm_password  = serializers.CharField(required=True, label="Confirm Password", style={'input_type': 'password'})

    def validate_confirm_password(self, value):
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
        username = self.validated_data['username']
        email    = self.validated_data['email']
        password = self.validated_data['password']
        user_obj = User(
                username = username,
                email = email,
            )
        user_obj.set_password(password)
        user_obj.is_active = False
        user_obj.save()
        return user_obj

class UserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # check the user for this uid is available or not in DB
        try:
            uid = decode_uid(self.initial_data.get("uid", ""))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError("we can't find any user with this token-uid" )

        if user is not None:
            is_token_valid = default_token_generator.check_token( user, validated_data["token"] )
        
        if is_token_valid:
            return user
        else:
            key_error = "invalid_token"
            raise serializers.ValidationError("activation token is not valid or your link is expired! request new one")

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
            raise serializers.ValidationError("user is not active.")

        return data

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    current_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate_new_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError("Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8))

        is_password_valid = self.context["request"].user.check_password(value)

        if is_password_valid:
            raise serializers.ValidationError("new password is already your old password")
        else:
            return value

    def validate_confirm_new_password(self, value):
        data = self.get_initial()
        new_password = data.get('new_password')
        if new_password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            raise serializers.ValidationError("current Passwords doesn't match.")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        return validated_data

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True, write_only=True, label="Email Address")
    username = serializers.CharField(required=False, allow_blank=True, write_only=True,)

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to reset your password.")

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
            raise serializers.ValidationError("we can't find any accout with this email or username")

        if user_obj.is_active:
            data["user"] = user_obj
        else:
            raise serializers.ValidationError("User not active.")
        return data

class ConfirmResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, label="Password", style={'input_type': 'password'})
    confirm_password = serializers.CharField(required=True, label="Confirm Password", style={'input_type': 'password'})

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError("Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8))
        return value

    def save(self):
        uid = self.validated_data['uid']
        token = self.validated_data['token']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        # check the user for this uid is available or not in DB
        try:
            uid = decode_uid(uid)
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError("we can't find any user with this token-uid")

        if user is not None:
            is_token_valid = default_token_generator.check_token( user, token )

        if is_token_valid:
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError( "token is not valid or your link is expired! request new one")

class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    class Meta:
        model = Token
        fields = ("auth_token",)
