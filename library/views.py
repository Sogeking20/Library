from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from .models import Book, BorrowedBook
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_catalog')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_catalog')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def book_catalog(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'book_catalog.html', {'books': books})

@login_required
def my_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, returned=False)
    return render(request, 'my_books.html', {'borrowed_books': borrowed_books})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.available:
        BorrowedBook.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
    return redirect('my_books')

@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = BorrowedBook.objects.get(id=borrowed_book_id, user=request.user)
    borrowed_book.returned = True
    borrowed_book.book.available = True
    borrowed_book.book.save()
    borrowed_book.save()
    return redirect('my_books')

@login_required
def debtors_list(request):
    if not request.user.is_librarian:
        return redirect('book_catalog')
    debtors = BorrowedBook.objects.filter(returned=False)
    return render(request, 'debtors_list.html', {'debtors': debtors})
