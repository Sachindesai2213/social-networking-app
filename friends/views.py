from rest_framework import viewsets
from .serializers import FriendSerializer, FriendRequestSerializer
from .models import Friend, FriendRequest
from .filters import FriendFilter, FriendRequestFilter
from main.mixins import PermissionMixin


# Create your views here.
class FriendViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing friend instances.
    """
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()
    filterset_class = FriendFilter

    def filter_queryset(self, queryset):
        # Filter out friends for Logged in user
        filter_queryset = super().filter_queryset(queryset)
        return filter_queryset.filter(user=self.request.user)


class FriendRequestViewSet(PermissionMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing friend requests instances.
    """
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    filterset_class = FriendRequestFilter

    def filter_queryset(self, queryset):
        # Filter out pending requests for Logged in user
        filter_queryset = super().filter_queryset(queryset)
        return filter_queryset.filter(
            to_user=self.request.user, status__isnull=True)
