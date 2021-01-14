from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.Serializer):
    Title = serializers.CharField()
    About = serializers.CharField()

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Title = validated_data.get('Title', instance.Title)
        instance.About = validated_data.get('About', instance.About)
        instance.save()
        return instance
