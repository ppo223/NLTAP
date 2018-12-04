from rest_framework import serializers
from .models import KeywordBase, Keyword


class KeywordBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordBase
        fields = '__all__'


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'