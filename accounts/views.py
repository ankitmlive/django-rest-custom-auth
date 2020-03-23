from accounts.models import MyUser
from accounts.email import ActivationEmail
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserActivationSerializer
from rest_framework import generics

from django.contrib.auth.models import update_last_login
from django.contrib.auth import login, logout, user_logged_in, user_logged_out

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.core.mail import send_mail
from accounts.compat import get_user_email

User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    """
    View responsible for new USER Registrartion
    """
    def post(self, request, format=None):
        response_data = {}
        serializer = UserRegistrationSerializer(data=request.data)
        permission_classes = (permissions.AllowAny,)
        if serializer.is_valid():
                account = serializer.save()
                response_data['response'] = 'successfully registered new user.'
                response_data['email'] = account.email
                response_data['username'] = account.username
                response_data['pk'] = account.pk
                token = Token.objects.get(user=account).key
                response_data['token'] = token

                #after creating user send and activation mail to user
                context = {"user": account}
                to = [get_user_email(account)]
                ActivationEmail(self.request, context).send(to)
        else:
            response_data = serializer.errors

        return Response(response_data)


class UserLoginAPIView(APIView):
    """
    View responsible for USER Login
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        response_data = {}
        serializer = UserLoginSerializer(data=request.data)
        permission_classes = (permissions.AllowAny,)
        if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                update_last_login(None, user)
                response_data['response'] = 'successfully logged in'
                response_data['email'] = user.email
                response_data['username'] = user.username
                response_data['pk'] = user.pk
                response_data['token'] = token.key
        else:
            response_data = serializer.errors

        return Response(response_data)


class UserActivationAPIView(APIView):
    """
     View responsible for USER Activation
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserActivationSerializer(data=request.data)
        permission_classes = (permissions.AllowAny,)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(sender=self.__class__, user=user, request=self.request)

        # if settings.SEND_CONFIRMATION_EMAIL:
        #     context = {"user": user}
        #     to = [get_user_email(user)]
        #     settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)
