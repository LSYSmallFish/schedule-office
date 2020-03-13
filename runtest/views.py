from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect

# Create your views here.
def TemplateView(request):
    print(1)
    return render(request, 'index.html')
