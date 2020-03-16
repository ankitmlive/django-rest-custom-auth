from accounts.models import MyUser
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
        queryset = MyUser.objects.all()
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class UserRegistrationAPIView(generics.CreateAPIView):
#     """
#     Endpoint for user registration.
#     """
#     queryset = MyUser.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = (permissions.AllowAny,)


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
