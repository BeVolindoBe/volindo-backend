from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    external_id = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'external_id',
        )
