from rest_framework import serializers
from .models import ModelTask, ModelTaskExecution


class ModelTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTask
        fields = '__all__'


class ModelTaskExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTaskExecution
        fields = '__all__'