from rest_framework import serializers
from accounts.models import MyUser
from django.conf import settings

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
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if MyUser.objects.filter(username=value).exists():
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
        user_obj = MyUser(
                username = username,
                email = email,
                fullname = fullname,
            )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj
   
