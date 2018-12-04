from rest_framework import serializers
from .models import AreaOfJob


class AreaOfJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfJob
        fields = '__all__'
