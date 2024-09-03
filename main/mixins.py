from rest_framework import (
    serializers, permissions, response, status, filters, pagination)
from django_filters import rest_framework as drf_filters


class CustomPagination(pagination.PageNumberPagination):
    '''Custom Pagination class'''
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 10
    page_query_param = 'page'


class SerializerMixin(metaclass=serializers.SerializerMetaclass):
    '''Custom Serializer Mixin'''

    class Meta:
        exclude = ['created_by']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['is_active'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        validated_data['modified_by'] = request.user
        return super().update(instance, validated_data)


class PermissionMixin:
    permission_classes = [
        permissions.IsAuthenticated
    ]
    pagination_class = CustomPagination
    filter_backends = [drf_filters.DjangoFilterBackend,
                       filters.SearchFilter]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        """
        Add request to serializer context.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
