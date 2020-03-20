from accounts.models import MyUser
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import generics

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

class UserRegistrationAPIView(generics.CreateAPIView):
    """
    View responsible for new USER Registrartion
    """
    def post(self, request, format=None):
        data = {}
        serializer = UserRegistrationSerializer(data=request.data)
        permission_classes = (permissions.AllowAny,)
        if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'successfully registered new user.'
                data['email'] = account.email
                data['username'] = account.username
                data['pk'] = account.pk
                token = Token.objects.get(user=account).key
                data['token'] = token
        else:
            data = serializer.errors

        return Response(data)


class UserLoginAPIView(APIView):
    """
    View responsible for USER Login
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}
        serializer = UserLoginSerializer(data=request.data)
        permission_classes = (permissions.AllowAny,)
        if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                data['response'] = 'successfully logged in'
                data['email'] = user.email
                data['username'] = user.username
                data['pk'] = user.pk
                data['token'] = token.key
        else:
            data = serializer.errors

        return Response(data)


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = MyUser.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
