from django.urls import path
from . import views

urlpatterns = [
    # Auth url's
    path('sign-up/', views.UserSignUpAPIView.as_view(), name='sign-up'),
    path('sign-in/', views.UserSignInAPIView.as_view(), name='sign-in'),
    path('sign-out/', views.UserSignOutAPIView.as_view(), name='sign-out'),
    path('activate-account/', views.UserActivationAPIView.as_view(), name='activate-account'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name="change-password"),
    path('reset-password/', views.ResetPasswordAPIView.as_view(), name="reset-password"),
    path('reset-password-confirm/', views.ConfirmResetPasswordAPIView.as_view(), name="reset-password-confirm"),
    path('hello/', views.HelloView.as_view(), name='hello'),
]