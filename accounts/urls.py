from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as tokenViews
from . import views

#router = routers.DefaultRouter()
#router.register(r'accounts', UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('', include(router.urls)),
    path('signup/', views.UserRegistrationAPIView.as_view(), name='sign-up'),
    path('signin/', views.UserLoginAPIView.as_view(), name='sign-in'),
    #path('signout/', views.UserLogoutAPIView.as_view(), name='sign-out'),
    path('get-token/', tokenViews.obtain_auth_token, name='get-token')
]

    # path("signup/", views.signup, name="account_signup"),
    # path("login/", views.login, name="account_login"),
    # path("logout/", views.logout, name="account_logout"),
    # path("password/change/", views.password_change,
    #      name="account_change_password"),
    # path("password/set/", views.password_set, name="account_set_password"),
    # path("inactive/", views.account_inactive, name="account_inactive"),

    # # E-mail
    # path("email/", views.email, name="account_email"),
    # path("confirm-email/", views.email_verification_sent,
    #      name="account_email_verification_sent"),
    # re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email,
    #         name="account_confirm_email"),

    # # password reset
    # path("password/reset/", views.password_reset,
    #      name="account_reset_password"),
    # path("password/reset/done/", views.password_reset_done,
    #      name="account_reset_password_done"),
    # re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
    #         views.password_reset_from_key,
    #         name="account_reset_password_from_key"),
    # path("password/reset/key/done/", views.password_reset_from_key_done,
    #      name="account_reset_password_from_key_done"),