from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LIBRARIAN = 'LIBRARIAN'
    READER = 'READER'
    ROLE_CHOICES = [
        (LIBRARIAN, 'Librarian'),
        (READER, 'Reader'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    employee_id = models.CharField(max_length=10, blank=True, null=True)  # Табельный номер для библиотекаря
    address = models.TextField(blank=True, null=True)  # Адрес для читателя

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_user_set',
        related_query_name='library_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_user_permissions',
        related_query_name='library_user_permissions',
    )

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def days_on_hand(self):
        from django.utils.timezone import now
        return (now() - self.borrowed_at).days