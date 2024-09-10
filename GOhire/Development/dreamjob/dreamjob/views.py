from django.shortcuts import render

def test_home(request):
    return render(request, 'test_home.html')
