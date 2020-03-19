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

# class UserLoginAPIView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#             serializer = self.serializer_class(data=request.data, context={'request': request})
#             serializer.is_valid(raise_exception=True)
#             user = serializer.validated_data['user']
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token': token.key,
#                 'user_id': user.pk,
#                 'email': user.email
#             })

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
            data = serializer.data
        else:
            data = serializer.errors

        return Response(serializer.data)
        #print(data)

# class AuthCustomTokenSerializer(serializers.Serializer):
#     email_or_username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         email_or_username = attrs.get('email_or_username')
#         password = attrs.get('password')

#         if email_or_username and password:
#             # Check if user sent email
#             if validateEmail(email_or_username):
#                 user_request = get_object_or_404(
#                     User,
#                     email=email_or_username,
#                 )

#                 email_or_username = user_request.username

#             user = authenticate(username=email_or_username, password=password)

#             if user:
#                 if not user.is_active:
#                     msg = _('User account is disabled.')
#                     raise exceptions.ValidationError(msg)
#             else:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = _('Must include "email or username" and "password"')
#             raise exceptions.ValidationError(msg)

#         attrs['user'] = user
#         return attrs
        




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
