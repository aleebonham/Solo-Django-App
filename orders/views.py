from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, Customer
from books.models import Book


def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        if not book_id:
            messages.error(request, "No book selected.")
            return redirect('book_list')
        book = get_object_or_404(Book, id=book_id)
        if quantity <1 or quantity > book.stock:
            messages.error(request, f"Invalid quantity. Max available:{book.stock}.")
            return redirect('book_detail', id=book.id)
        cart = request.session.get('cart', {})
        cart[book_id] = cart.get(book_id, 0) + quantity
        request.session['cart'] = cart
        messages.success(request, f"Added {quantity} x {book.title} to cart.")
        return redirect('cart')
    return redirect('book_list')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            subtotal = book.price * quantity
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total_price += subtotal
        except Book.DoesNotExist:
            continue
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'orders/cart.html', context)


@login_required
def checkout(request):
    """Display and process the checkout page."""
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email or 'default@example.com'
        )
        messages.info(request, "Customer profile created for you.")

    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    cart_items = []
    total_price = 0
    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            subtotal = book.price * quantity
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total_price += subtotal
        except Book.DoesNotExist:
            continue

    if request.method == 'POST':
        order = Order.objects.create(
            customer=customer,
            total_price=total_price,
            status='pending'
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item['book'],
                quantity=item['quantity'],
                price=item['subtotal']
            )
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'customer': customer,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    """Display the user's order history."""
    orders = Order.objects.filter(customer__user=request.user).order_by('-created_date')
    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)
