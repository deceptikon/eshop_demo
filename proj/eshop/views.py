from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.
def index(request):
    return render(request, 'main.html')

def cats(request, slug):
    p = Product.objects.all()
    print(">>>>>>", slug)
    context = { 'p': p }
    return render(request, 'cats.html', context)
