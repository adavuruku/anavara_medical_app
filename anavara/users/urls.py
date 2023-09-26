from django.urls import path
from users.views import MyObtainTokenPairView, RegisterView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('change-password/', ChangePasswordView.as_view(), name='user_change_password'),
]