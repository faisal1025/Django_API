from rest_framework import serializers
from api.models import AudioModel, Duration
from rest_framework.response import Response

# create serializers here

class DurationSerializer(serializers.ModelSerializer):
    startTime=serializers.IntegerField()
    endTime=serializers.IntegerField()
    class Meta:
        model = Duration
        fields = ('startTime', 'endTime')

class AudioSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    duration = DurationSerializer()
    class Meta:
        model = AudioModel
        fields = ('id', 'url', 'volume', 'type', 'video_component_id', 'duration')

    def create(self, validated_data):
        duration_data = validated_data.pop('duration', None)
        audio = AudioModel.objects.create(**validated_data)
        print(duration_data)
        if duration_data:
            Duration.objects.create(audio=audio, **duration_data)
        return audio