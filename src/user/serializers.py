from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    user_status = ItemSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('user_status', )
