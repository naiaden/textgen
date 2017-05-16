from django.shortcuts import render


def index(request):
    return render(request, 'rain/index.html', {'foo': 'bar',})
