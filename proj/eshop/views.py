from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


from .models import Product, Category, Cart, CartContent
from .forms import RegisterForm, LoginForm

# Create your views here.
def index(request):
    return render(request, 'main.html')

def cats(request, slug=None):
    cats = Category.objects.all()
    if slug:
        selected_cat = Category.objects.get(slug=slug)
        products = Product.objects.filter(category_id=selected_cat.id).all()
    else:
        products = Product.objects.all()

    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    try:
        cart = Cart.objects.get(session_key=session_key)
    except ObjectDoesNotExist:
        cart = Cart(
            session_key = session_key,
            total_cost = 0
        )
        cart.save()

    cart_records = CartContent.objects.filter(cart_id=cart.id)

    if request.GET and 'buy' in request.GET:
        product_id = int(request.GET['buy'])
        prod = Product.objects.get(id=product_id)
        try:
            cart_record = CartContent.objects.get(cart_id=cart.id, product_id=product_id)
            cart_record.quantity = cart_record.quantity + 1
        except ObjectDoesNotExist:
            cart_record = CartContent(
                product = prod,
                cart = cart,
                quantity = 1
            )
        cart_record.save()
        return redirect('products_category', slug=slug)
    elif request.GET and 'action' in request.GET:
        if request.GET['action'] == 'clear_cart':
            cart.delete()
            return redirect('products_category', slug=slug) if slug else redirect('products_category_all')

    context = { 'cats': cats, 'products': products,  'cart_records': cart_records }
    return render(request, 'cats.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('products_category_all')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET and 'next' in request.GET:
                    return redirect(request.GET['next'])
                return redirect('products_category_all')
            else:
                form.add_error('login', 'Bad login or password')
                form.add_error('password', 'Bad login or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', { 'form': form })

def log_out(request):
    logout(request)
    return redirect('products_category_all')

@login_required()
def protected(request):
    return HttpResponse(str(request.user))
