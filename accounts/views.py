from accounts.email import ActivationEmail, ConfirmationEmail, PasswordChangedConfirmationEmail, PasswordResetEmail
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer, ResetPasswordSerializer, ConfirmResetPasswordSerializer, UserActivationSerializer, UserSerializer, UserAvatarSerializer

from rest_framework import generics
from django.contrib.auth.models import update_last_login
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import parsers
from rest_framework import decorators

from django.contrib.auth import get_user_model
from accounts import signals
from django.contrib.auth.signals import user_logged_in

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes


from accounts.utils import get_user_email

User = get_user_model()

#--> User List view
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_instance(self):
        return self.request.user

    @decorators.action(
        detail=True,
        methods=['PUT'],
        serializer_class=UserAvatarSerializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def avatar(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        detail=False,
        methods=["get", "put", "patch",],
        serializer_class=UserSerializer,
        permission_classes = [IsAuthenticated]
    )
    def auth(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)

#--> auth view
class UserSignUpAPIView(generics.CreateAPIView):
    """
    View responsible for new USER Registrartion
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                account = serializer.save()
                response_data['response'] = 'successfully registered new user.'
                response_data['email'] = account.email
                response_data['username'] = account.username
                response_data['pk'] = account.pk
                signals.user_registered.send(sender=self.__class__, user=account, request=self.request)
                #after creating user send and activation mail to user
                context = {"user": account}
                to = [get_user_email(account)]
                ActivationEmail(self.request, context).send(to)
        else:
            response_data = serializer.errors

        return Response(response_data)

class UserSignInAPIView(ObtainAuthToken):
    """
    View responsible for USER Login
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response_data = {}
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                update_last_login(None, user)
                response_data['details'] = 'successfully logged in'
                # response_data['email'] = user.email
                # response_data['fullname'] = user.fullname
                # response_data['username'] = user.username
                # response_data['avatar'] = request.build_absolute_uri(user.avatar.url)
                #response_data['pk'] = user.pk
                response_data['token'] = token.key
        else:
            response_data = serializer.errors

        return Response(response_data)

class UserSignOutAPIView(APIView):
    """
    View responsible for USER Signout
    later there is a need of serializer implementaion
    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        response_data = {}
        data = Token.objects.filter(user=request.user).delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        response_data['response'] = 'user successfully logged out'
        return Response(response_data)

class UserActivationAPIView(APIView):
    """
     View responsible for USER Activation
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response_date = {}
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            user.is_active = True
            user.email_verified = True
            user.save()
            signals.user_activated.send(sender=self.__class__, user=user, request=self.request)
            context = {"user": user}
            to = [get_user_email(user)]
            ConfirmationEmail(self.request, context).send(to)
            response_date["response"] = "user activated succefully"
        else:
            response_date = serializer.errors
        return Response(response_date)

class ChangePasswordAPIView(APIView):
    """
    View responsible for USER password change
    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        response_data = {}
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request.auth})
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            new_password = data["new_password"]
            self.request.user.set_password(new_password)
            self.request.user.save()
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            PasswordChangedConfirmationEmail(self.request, context).send(to)
            response_data["response"] = "password changed successfully"
        else:
            response_data = serializer.errors
        return Response(response_data)

class ResetPasswordAPIView(APIView):
    """
    View responsible for USER password reset
    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response_data = {}
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            if user:
                context = {"user": user}
                to = [get_user_email(user)]
                PasswordResetEmail(self.request, context).send(to) 
                response_data["response"] = "password reset link has been sent"
        else:
            response_data = serializer.errors
        return Response(response_data)

class ConfirmResetPasswordAPIView(APIView):
    """
    View responsible for USER password reset confirmation
    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response_data = {}
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            context = {"user": user}
            to = [get_user_email(user)]
            PasswordChangedConfirmationEmail(self.request, context).send(to)
            response_data['response'] = 'password reset done successfully.'
        else:
            response_data = serializer.errors
        return Response(response_data)

#test view
class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user), 
            'auth': str(request.auth), 
        }
        return Response(content)