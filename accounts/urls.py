from django.urls import path
from . import views

urlpatterns = [
    # Auth url's
    path('sign-up/', views.UserSignUpView.as_view(), name='sign-up'),
    path('sign-in/', views.UserSignInView.as_view(), name='sign-in'),
    path('sign-out/', views.UserSignOutView.as_view(), name='sign-out'),
    path('activate-account/', views.UserActivationView.as_view(), name='activate-account'),
    path('change-password/', views.ChangePasswordView.as_view(), name="change-password"),
    path('reset-password/', views.ResetPasswordView.as_view(), name="reset-password"),
    path('reset-password-confirm/', views.ConfirmResetPasswordView.as_view(), name="reset-password-confirm"),
    path('hello/', views.HelloView.as_view(), name='hello'),

    #
    path('check_username/', views.CheckUsernameView.as_view(), name="check_username"),
]