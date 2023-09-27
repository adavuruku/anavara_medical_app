from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
# Create your views here.
from .serializers import MyTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .permission import CanCreateMedicalRecord

# for overriding the usermodel
from django.contrib.auth import get_user_model
User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    # permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    permission_classes = (CanCreateMedicalRecord,)
    serializer_class = UserSerializer

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,CanCreateMedicalRecord,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # log user out of all device
        tokens = OutstandingToken.objects.filter(user_id=user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(serializer.get_auth_token(user), status=status.HTTP_200_OK)