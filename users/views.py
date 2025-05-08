from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orders.models import Order 
from django.db.models import Count, Sum

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'users/register.html')

@login_required
def dashboard(request):
    orders = Order.objects.filter(customer__user=request.user).values('created_date__date').annotate(total=Count('id'))
    data = {'labels': [o['created_date__date'].strftime('%Y-%m-%d') for o in orders],
            'values': [o['total'] for o in orders]}
    return render(request, 'users/dashboard.html', {'data': data})

@login_required
def user_logout(request):
    logout(request)
    return redirect('book_list')