from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import AudioViewSet

routes = routers.DefaultRouter()
routes.register(r'audio', AudioViewSet)

urlpatterns = [
    path('', include(routes.urls)),
    path('audio/getFragment/<int:start>/<int:end>/', views.AudioViewSet.as_view({'get': 'getFragment'}), name='audio-getFragment'),
]
