from rest_framework import serializers
from .models import Book, BorrowedBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre']

class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'borrowed_at']
