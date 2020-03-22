from accounts.models import MyUser
from accounts.email import ActivationEmail
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer
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

# class UserLogoutAPIView(APIView):
#     """
#     Use this endpoint to logout user (remove user authentication token).
#     not working yet
#     """

#     authentication_classes = []
#     #permission_classes = [permissions.IsAuthenticated,]

#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)
