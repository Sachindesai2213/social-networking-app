from rest_framework import viewsets, status, response
from .serializers import UserSerializer
from .models import User
from main.mixins import PermissionMixin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return response.Response(
                {"error": "Email is mandatory"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Custom authentication logic
        user = authenticate(email=email.lower(), password=password)
        if not user:
            return response.Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return response.Response({
            'refresh': str(refresh),
            'access': access_token,
        })


class SignupViewSet(viewsets.ModelViewSet):
    """
    A viewset for creating user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['post']
    permission_classes = []
    authentication_classes = []


class UserViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    search_fields = ['=email', 'first_name', 'last_name']

    def filter_queryset(self, queryset):
        # Exclude Logged in user
        filter_queryset = super().filter_queryset(queryset)
        return filter_queryset.exclude(id=self.request.user.id)
