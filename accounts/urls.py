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
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('get-token/', tokenViews.obtain_auth_token, name='get-token')
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', views.LogoutView.as_view(), name='logout'),
#     path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
#     path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
#     path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]