from accounts.models import MyUser
from rest_framework.authtoken.models import Token
from accounts.serializers import UserRegistrationSerializer
from rest_framework import generics

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

class UserRegistrationAPIView(generics.CreateAPIView):
    """
    List all snippets, or create a new snippet.
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

# class UserLoginAPIView(APIView):
#     """
#     View responsible for USER Login
#     """
#     authentication_classes = []
# 	permission_classes = []

#     def post(self, request):
#         data = {}
#         serializer = UserLoginSerializer(data=request.data)
#         permission_classes = (permissions.AllowAny,)
#         if serializer.is_valid():
#                 account =   serializer.save()
#                 #..... on progress
        




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
