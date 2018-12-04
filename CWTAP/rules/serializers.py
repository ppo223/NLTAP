from rest_framework import serializers
from .models import RuleBase, Rule


class RuleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleBase
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
