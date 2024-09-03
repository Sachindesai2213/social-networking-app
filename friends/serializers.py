from datetime import datetime, timedelta
from rest_framework import serializers, status, validators
from .models import Friend, FriendRequest
from main.mixins import SerializerMixin


class FriendSerializer(SerializerMixin, serializers.ModelSerializer):

    class Meta(SerializerMixin.Meta):
        model = Friend


class FriendRequestSerializer(SerializerMixin, serializers.ModelSerializer):

    class Meta(SerializerMixin.Meta):
        model = FriendRequest

    def validate(self, attrs):
        request = self.context.get('request', {})
        to_datetime = datetime.now()
        from_datetime = to_datetime - timedelta(minutes=1)
        requests_sent = FriendRequest.objects.filter(
            created_on__range=[from_datetime, to_datetime],
            created_by=request.user
        )
        if self.instance and requests_sent.count() >= 3:
            raise serializers.ValidationError(
                'Limit exceeded for sending Friend Requests',
                status.HTTP_400_BAD_REQUEST
            )
        if self.instance and self.instance.status:
            statuses = {'A': 'Accepted', 'R': 'Rejected'}
            current_status = statuses.get(self.instance.status, 'Attempted')
            raise serializers.ValidationError(
                f'Request already {current_status}',
                status.HTTP_400_BAD_REQUEST
            )
        return super().validate(attrs)

    def to_internal_value(self, data):
        request = self.context.get('request', {})
        friend_request_data = data.copy()
        if not self.instance:
            friend_request_data['from_user'] = request.user.id
        else:
            if friend_request_data['status'] == 'A':
                Friend.objects.bulk_create([
                    Friend(
                        user=self.instance.from_user,
                        friend=self.instance.to_user,
                        created_by=request.user
                    ),
                    Friend(
                        user=self.instance.to_user,
                        friend=self.instance.from_user,
                        created_by=request.user
                    )
                ])
        return super().to_internal_value(friend_request_data)
