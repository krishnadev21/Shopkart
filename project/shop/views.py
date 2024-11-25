from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Category, Product, Cart, Favourite
from .forms import CustomUserModel
from django.contrib import messages
from django.http import JsonResponse
import json

def home(request):
    # Get trending products
    trending_products = Product.objects.filter(trending=1) 
    return render(request, 'shop/index.html', context={'trending_products' : trending_products})

def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) # Log the user in
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        
        messages.error(request, 'Invalid login credentials. Please try again.')
        return redirect('login')
    
    return render(request, 'shop/login.html', context={})

def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have successfully logged out.')
    return redirect('home')

def register(request):
    form = CustomUserModel()
    if request.method == 'POST':
        form = CustomUserModel(request.POST) # Bind POST data to the form
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in to continue.')
            return redirect('login')
        
        messages.error(request, 'Unable to create an account. Please check your details and try again.')
        return redirect('register')

    return render(request, 'shop/register.html', context={'form' : form})

def cart(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.info(request, 'Log in to see what"s in your cart')
        return redirect('login')
    
    cart_products = Cart.objects.filter(user=request.user)
    return render(request, 'shop/cart.html', context={'cart' : cart_products})
    

def addToCart(request):
    # Ensure the request is an AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'Status': False, 'Body': 'Invalid access.'}, status=400)

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'Status': False, 'Body': 'Login to add favourite.'}, status=401)
    
    # Parse the JSON data from the request
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product_quantity = data.get('product_quantity')

    # Check if the product exists
    if not Product.objects.filter(id=product_id).exists():
        return JsonResponse({'Status' : False, 'Body' : 'Product not available.'}, status=400)
    
    # Check if the product is already in the cart
    if Cart.objects.filter(user=request.user, product=product_id).exists():
        return JsonResponse({'Status' : True, 'Body' : 'Product already in cart.'}, status=200)
    
    # Check product stock availability
    if product_quantity >= Product.objects.get(id=product_id).quantity:
        return JsonResponse({'Status' : False, 'Body' : f'Insufficient stock. Available stock: {Product.objects.get(id=product_id).quantity}'}, status=400)
    
    # Add the product to the cart
    Cart.objects.create(user_id=request.user.id, product_id=product_id, product_quantity=product_quantity)
    return JsonResponse({'Status' : True, 'Body' : 'Product added to cart.'}, status=200)
    
def removeCart(request, pk):
    Cart.objects.get(id=pk).delete()
    return redirect('cart')

def collection(request):
    category = Category.objects.filter(status=0)
    return render(request, 'shop/collection.html', context={'category' : category})

def collectionView(request, name):
    # Check if the category exists and is active (status=0)
    if not Category.objects.filter(name=name, status=0).exists():  # Get active categories
        messages.warning(request, 'No such category found.')
        return redirect('collections')
    
    products = Product.objects.filter(category__name=name)
    return render(request, 'shop/products/index.html', context={'products' : products, 'category_name' : name})
    
def productDetails(request, cname, pname):
     # Check if category exists and is active
    if not Category.objects.filter(name=cname, status=0).exists(): 
        messages.error(request, 'No such category found.')
        return redirect('collections')

    # Check if product exists and is active
    if not Product.objects.filter(name=pname, status=0).exists():  
        messages.error(request, 'No such product found.')
        return redirect('collections')
    
    # Get the product
    product = Product.objects.filter(name=pname, status=0).first()  
    return render(request, 'shop/products/product_details.html', context={'product' : product})

def favourities(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Log in to see your saved favourites')
        return redirect('login')
    
    fav_products = Favourite.objects.filter(user=request.user)
    return render(request, 'shop/favourites.html', context={'fav_products':fav_products})

def addToFav(request):
    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'Status': False, 'Body': 'Invalid access.'}, status=400)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'Status': False, 'Body': 'Login to add favourite.'}, status=401)

    # Parse the JSON data from the request
    data = json.loads(request.body)
    product_id = data.get('product_id')

    # Check if the product exists
    if not Product.objects.filter(id=product_id).exists():
        return JsonResponse({'Status': False, 'Body': 'Product not available.'}, status=400)

    # Check if the product is already in favourites
    if Favourite.objects.filter(user=request.user, product_id=product_id):
        return JsonResponse({'Status': False, 'Body': 'Product already in favourites.'}, status=200)

    # Add the product to favourites
    Favourite.objects.create(user=request.user, product_id=product_id)
    return JsonResponse({'Status': True, 'Body': 'Product added to favourite.'}, status=200)

def removeFavourite(request, pk):
    Favourite.objects.get(id=pk).delete()
    return redirect('favourities')