from books.models import Book
from faker import Faker

fake = Faker()
print("Before:", list(Book.objects.values('title', 'author')[:5]))
books = Book.objects.filter(author='Unknown Author')
for book in books:
    book.author = fake.name()
Book.objects.bulk_update(books, ['author'])
print("After:", list(Book.objects.values('title', 'author')[:5]))
