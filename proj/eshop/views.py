from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


from .models import Product, Category, Cart, CartContent
from .forms import RegisterForm, LoginForm

# Create your views here.
class MasterView(TemplateView):
    def get_cart_records(self, the_cart=None):
        cart = self.get_cart() if the_cart is None else the_cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []
        return cart_records

    def get_cart(self):
        cart = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(
                    user_id=user_id,
                    total_cost=0
                )
                cart.save()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(
                    session_key=session_key,
                    total_cost=0
                )
                cart.save()
        return cart

class CatsView(MasterView):

    def get(self, request, slug=None):
        cats = Category.objects.all()
        print(slug)
        if slug:
            selected_cat = Category.objects.get(slug=slug)
            products = Product.objects.filter(category_id=selected_cat.id).all()
        else:
            products = Product.objects.all()

        cart_records = self.get_cart_records()
        cart = self.get_cart()

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
            return redirect('products_category', slug=slug) if slug else redirect('products_category_all')
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
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('products_category_all')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('products_category_all')

@login_required()
def protected(request):
    return HttpResponse(str(request.user))


class LoginView(MasterView):
    view_form = LoginForm
    login_template = 'login.html'

    def post(self, request):
        form = self.view_form(request.POST)
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

    def get(self, request):
        form = self.view_form()
        return render(request, self.login_template, { 'form': form })

class CartView(MasterView):

    request = None

    def get(self, request):
        self.request = request

        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        print(cart_total)
        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'cart.html', context)




