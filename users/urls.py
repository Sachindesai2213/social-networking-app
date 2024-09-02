from django.urls import path
from rest_framework import routers
from .views import LoginView, UserViewSet, SignupViewSet

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('signup', SignupViewSet, basename='signup')

urlpatterns += router.urls
