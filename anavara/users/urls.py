from django.urls import path
from users.views import MyObtainTokenPairView, RegisterView, ChangePasswordView, RequestPasswordResetEmail, SetNewPasswordAPIView, PasswordTokenCheckAPI
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='user_register'),
    path('change-password', ChangePasswordView.as_view(), name='user_change_password'),
    
    path('reset-password', RequestPasswordResetEmail.as_view(), name='user_reset_password'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),

    
]