from rest_framework import serializers

from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    notification_type = serializers.CharField(source='get_notification_type_display')

    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            'message',
            'priority',
            'notification_type',
            'read',
            'action',
            'updated_at',
            'created_at',
        )

        read_only_fields = (
            'id',
            'title',
            'message',
            'priority',
            'notification_type',
            'action',
            'updated_at',
            'created_at',
        )
