from rest_framework import serializers

from .models import Background


class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = [
            "id",
            "image",
            "color",
            "description",
            "url",
            "width",
            "height",
            "created_at",
        ]
