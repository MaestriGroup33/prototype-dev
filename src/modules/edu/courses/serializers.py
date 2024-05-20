from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "cod",
            "name",
            "description",
            "duration",
            "type",
            "area",
            "information",
            "objective",
            "jobmarket",
            "specifics",
            "curriculum",
            "avatar",
        ]
