
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("This is Home Page go to 'api/audio' to rest the rest_framework API")