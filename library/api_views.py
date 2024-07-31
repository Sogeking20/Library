from rest_framework import generics, serializers
from .models import Book, BorrowedBook
from .serializers import BookSerializer, BorrowedBookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowBookView(generics.CreateAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.available:
            book.available = False
            book.save()
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("Book is not available")

class ReturnBookView(generics.UpdateAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.returned = True
        instance.book.available = True
        instance.book.save()
        instance.save()
        return Response({"status": "book returned"})
