from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.CharField(max_length=50)
    isbn = models.CharField(max_length=15)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.title