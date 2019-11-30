from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

# Create your views here.
def index(request):
    return render(request, 'main.html')

def cats(request, slug=None):
    cats = Category.objects.all()
    if slug:
        selected_cat = Category.objects.get(slug=slug)
        products = Product.objects.filter(category_id=selected_cat.id).all()
    else:
        products = []

    print(">>>>>>", slug, cats)
    context = { 'cats': cats, 'products': products }
    return render(request, 'cats.html', context)
