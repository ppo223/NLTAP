from rest_framework import serializers
from .models import CorpusBase, Corpus


class CorpusBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusBase
        fields = '__all__'


class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = '__all__'
