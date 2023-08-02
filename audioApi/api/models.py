from typing import Any
from django.db import models

# Create your models here.
TYPE_TUPLE = [
    ('vo', 'vo'),
    ('bg_music', 'bg_music'),
    ('video_music', 'video_music')
]
class AudioModel(models.Model):
    url = models.CharField(max_length=50, null=True)
    volume = models.IntegerField()
    type = models.CharField(max_length=50, choices=TYPE_TUPLE)
    video_component_id = models.IntegerField(null=True)

class Duration(models.Model):
    audio = models.OneToOneField(AudioModel, related_name='duration', on_delete=models.CASCADE)
    startTime=models.IntegerField()
    endTime=models.IntegerField()
    


