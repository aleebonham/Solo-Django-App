from django.test import TestCase
from .models import Customer, Order, OrderItem
from books.models import Book
from django.contrib.auth.models import User


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@example.com')
        self.book = Book.objects.create(title='Test Book', author='Test Author', year=2020, genre='Fiction', isbn='1234567890123', stock=10)
        self.order = Order.objects.create(customer=self.customer, status='pending')

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(order=self.order, book=self.book, quantity=2)
        self.assertEqual(order_item.quantity, 2)