from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Avg
from .models import Product, Rating  

def home(request):
    products = Product.objects.annotate(average_rating=Avg('rating__rating'))
    rating_range = range(1, 11)
    return render(request, 'home.html', {'products': products, 'rating_range': rating_range})

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def add_rating(request, product_id):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))
        product = Product.objects.get(pk=product_id)
        Rating.objects.create(product=product, rating=rating_value)
    return redirect('home')

# Create your views here.
