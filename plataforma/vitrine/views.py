from django.shortcuts import render


def showcase(request):
    return render(request, 'showcase.html')
