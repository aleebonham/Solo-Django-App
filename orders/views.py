from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from books.models import Book


def cart(request):
    cart = request.session.get('cart', {})
    books = Book.objects.filter(id__in=cart.keys())
    cart_items = [(book, cart[str(book.id)]) for book in books]
    return render(request, 'orders/cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[book_id] = cart.get(book_id, 0) + quantity
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')
        customer = request.user.customer
        order = Order.objects.create(customer=customer, status='completed')
        for book_id, quantity in cart.items():
            book = Book.obects.get(id=book_id)
            OrderItem.obects.create(order=order, book=book, quantity=quantity)
            book.stock -= quantity
            book.save()
        request.session['cart'] = {}
        return redirect('book_list')
    return render(rerquest, 'orders/checkout.html')