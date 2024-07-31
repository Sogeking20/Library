from django.urls import path
from . import views
from .api_views import BookListView, BorrowBookView, ReturnBookView

urlpatterns = [
    path('register/', views.register, name='registration'),
    path('login/', views.user_login, name='login'),
    path('catalog/', views.book_catalog, name='book_catalog'),
    path('my_books/', views.my_books, name='my_books'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrowed_book_id>/', views.return_book, name='return_book'),
    path('debtors/', views.debtors_list, name='debtors_list'),
    
    path('api/books/', BookListView.as_view(), name='api_book_list'),
    path('api/borrow/', BorrowBookView.as_view(), name='api_borrow_book'),
    path('api/return/<int:pk>/', ReturnBookView.as_view(), name='api_return_book'),
]
