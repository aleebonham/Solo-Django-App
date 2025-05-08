from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Book
from orders.models import Customer, Order, OrderItem
from django.contrib.auth.models import User
import random
import csv
import os

class Command(BaseCommand):
    help = 'Load sample book and order data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        Book.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()
        User.objects.filter(is_staff=False).delete()

        csv_path = os.path.join(os.path.dirname(__file__), '../../../data/openlibrary_subset.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    Book.objects.create(
                        title=row['title'],
                        author=row['author'],
                        year=int(row['year']),
                        genre=row['genre'],
                        isbn=row['isbn'],
                        stock=random.randint(5, 20)
                    )
        else:
            #fake book data
            genres = ['Fiction', 'Non-Fiction', 'Sci-Fi', 'Fantasy', 'Mystery']
            for _ in range(5000):
                Book.objects.create(
                    title=fake.sentence(nb_words=4),
                    author=fake.name(),
                    year=random.randint(1900, 2025),
                    genre=random.choice(genres),
                    isbn=fake.isbn13(),
                    stock=random.randint(5, 20)
                )

        # fake customers and orders
        for _ in range(100):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                password='password123',
                email=fake.email()
            )
            customer = Customer.objects.create(
                user=user,
                name=fake.name(),
                email=user.email
            )
            for _ in range(random.randint(1, 5)):
                order = Order.objects.create(customer=customer, status='completed')
                books = random.sample(list(Book.objects.all()), random.randint(1, 3))
                for book in books:
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=random.randint(1, min(book.stock, 5))
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))