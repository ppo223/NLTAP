from rest_framework import serializers
from .models import LabelBase, Label


class LabelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelBase
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
