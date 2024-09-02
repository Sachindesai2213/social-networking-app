from django_filters import rest_framework as drf_filters
from .models import Friend, FriendRequest


# Create your filters here.
class FriendFilter(drf_filters.FilterSet):

    class Meta:
        model = Friend
        fields = ['user', 'friend']


class FriendRequestFilter(drf_filters.FilterSet):
    status = drf_filters.CharFilter(method='status_filter')

    class Meta:
        model = FriendRequest
        fields = ['from_user', 'to_user', 'status']

    def status_filter(self, queryset, name, value):
        print(value, queryset)
        if value == 'P':
            return queryset.filter(status__isnull=True)
        return queryset.filter(status=value)
