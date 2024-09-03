from rest_framework import serializers, validators
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        validators = [
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exists",
                lookup='email'
            )
        ]
