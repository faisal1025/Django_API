from django.shortcuts import render
from rest_framework import viewsets
from api.models import AudioModel
from rest_framework.response import Response
from rest_framework import status
from api.serializers import AudioSerializer
from django.db.models import Q
from rest_framework.decorators import action
import random
# Create your views here.

class AudioViewSet(viewsets.ModelViewSet):
    queryset = AudioModel.objects.all()
    serializer_class = AudioSerializer

    # api/audio/getFragment/<int:start>/<int:end>/
    @action(detail=True, methods=['get'])
    def getFragment(self, request, start, end):
        fragment_elements = AudioModel.objects.filter(
            Q(duration__startTime__lt=end) & 
            Q(duration__endTime__gt=start)
        )
        fragment_elements_serializer = AudioSerializer(fragment_elements, many=True, context={'request':request})
        return Response(fragment_elements_serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check for overlapping elements of the same type
            audio_type = serializer.validated_data['type']
            start_time = serializer.validated_data['duration']['startTime']
            end_time = serializer.validated_data['duration']['endTime']
            # print(end_time, '  ', start_time)

            overlapping_elements = AudioModel.objects.filter(
                type=audio_type
            )
            
            if overlapping_elements.exists():
                num = end_time-start_time
                for elements in overlapping_elements:
                    audio = AudioSerializer(elements).data
                    if start_time >= audio['duration']['endTime'] or end_time <= audio['duration']['startTime']:
                        continue
                    start_time = audio['duration']['endTime']  
                    end_time = start_time+num     

            overlapping_elements = AudioModel.objects.filter(
                ~Q(type=audio_type) & 
                Q(duration__startTime__lt=end_time) & 
                Q(duration__endTime__gt=start_time)
            )
            
            
            partition1 = start_time
            partition2 = end_time
            if overlapping_elements.exists():
                # Handle overlapping elements here
                for elements in overlapping_elements:
                    audio = AudioSerializer(elements).data
                    partition2 = min(partition2, audio['duration']['endTime']) 
                    partition1 = max(partition1, audio['duration']['startTime'])
                    
                    
            serializer1 = self.get_serializer(data=request.data)
            serializer2 = self.get_serializer(data=request.data)
            if serializer1.is_valid():
                serializer1.validated_data['duration']['startTime'] = start_time
                serializer1.validated_data['duration']['endTime'] = partition1
                serializer1.validated_data['volume'] = 100
            if serializer.is_valid():
                serializer.validated_data['duration']['startTime'] = partition1
                serializer.validated_data['duration']['endTime'] = partition2
                serializer.validated_data['volume'] = random.randint(2, 95)
            if serializer2.is_valid():
                serializer2.validated_data['duration']['startTime'] = partition2
                serializer2.validated_data['duration']['endTime'] = end_time
                serializer2.validated_data['volume'] = 100
            # serializer.validated_data['duration']['startTime'] = start_time
            # serializer.validated_data['duration']['endTime'] = end_time
            if start_time < partition1:
                serializer1.save()
            if partition1 < partition2:
                serializer.save()
            if partition2 < end_time:
                serializer2.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)