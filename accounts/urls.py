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
    path('signup/', views.UserSignUpAPIView.as_view(), name='sign-up'),
    path('signin/', views.UserSignInAPIView.as_view(), name='sign-in'),
    path('signout/', views.UserSignOutAPIView.as_view(), name='sign-out'),

    path('activate/', views.UserActivationAPIView.as_view(), name='user-activate'),
    path('hello/', views.HelloView.as_view(), name='hello'),

    #path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    #path('get-token/', tokenViews.obtain_auth_token, name='get-token')
]