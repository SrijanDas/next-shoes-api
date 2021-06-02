from django.http import HttpResponse

def index(request):
    return HttpResponse("API in running. Go to: 'api/v1'")