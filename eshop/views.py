from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProductForm, UserRegistrationForm
from .models import Product

# Create your views here.

def home(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {"products": products, "query": query}
    template = (
        "partials/vehicle_results.html"
        if request.headers.get("HX-Request") == "true"
        else "index.html"
    )
    return render(request, template, context)

@staff_member_required(login_url="login")
def add_products(request):
    if request.method=="POST":
        form = ProductForm(request.POST,request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, "New item added.")
            return redirect('product')
        
            
    else:
        form =ProductForm()    
        
    return render(request,'add_product.html',{'form':form})
#read CRUD -fetch all records then display 
@staff_member_required(login_url="login")
def products(request):
    Products = Product.objects.all()
    
    return render(request,'admin_dashboard.html',{'myproduct': Products})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        account = User.objects.filter(email__iexact=email).first() if email else None
        user = (
            authenticate(request, username=account.username, password=password)
            if account and password
            else None
        )

        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html", {"email": email})
        if user.is_staff:
            auth_login(request,user)
            return redirect("product")
        else:
            auth_login(request, user)
            return redirect("home")
        
    return render(request,'login.html')

def reset_password(request):
    return render(request,"reset.html")
    


@require_POST
def logout_user(request):
    auth_logout(request)
    return redirect("home")

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please sign in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})
    

@staff_member_required(login_url="login")
def delete_product(request,id):
    prod= get_object_or_404(Product,id=id)
    prod.delete()
    messages.success(request, "Selected item deleted.")
    
    return redirect('product')


@staff_member_required(login_url="login")
def edit_product(request,id):
    prod = get_object_or_404(Product,id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "Product updated.")
            else:
                messages.info(request, "No changes were made.")
            return redirect("product")
    else:
        form = ProductForm(instance=prod)

    return render(request, "edit_product.html", {"form": form, "product": prod})


