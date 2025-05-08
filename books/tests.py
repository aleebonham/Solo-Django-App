from django.test import TestCase
from .models import Book

class BookModelTests(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            year=2020,
            genre="Fiction",
            isbn="1234567890123",
            stock=10
        )
        self.assertEqual(book.title, "Test Book")