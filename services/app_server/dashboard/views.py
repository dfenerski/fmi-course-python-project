# type: ignore

from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse('Charts are being loaded...')
