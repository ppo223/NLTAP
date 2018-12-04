from rest_framework import serializers
from .models import Meta


class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = '__all__'
