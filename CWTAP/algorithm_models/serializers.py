from rest_framework import serializers
from .models import ModelBase, Model, ModelInstance


class ModelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelBase
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class ModelInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelInstance
        fields = '__all__'
