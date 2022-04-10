# from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'books': books})

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == 'POST':
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category)
        books.save()
        alert = True
        return render(request, 'library/add_book.html', {'alert':alert})
    return render(request, 'library/add_book.html')

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, 'library/view_books.html', {'books':books})

@login_required(login_url = '/admin_login')
def update_book(request, myid):
    books = Book.objects.get(id = myid)
    if request.method == 'POST':
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']

        books.name = name
        books.author = author
        books.isbn = isbn
        books.category = category      
        books.save()
        alert = True
        return redirect('/view_books', {'alert':alert})
    return render(request, 'library/update_book.html', {'books': books})


def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect('/view_books')


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, 'library/change_password.html', {'alert':alert})
            else:
                currpasswrong = True
                return render(request, 'library/change_password.html', {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, 'library/change_password.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('/view_books')
            else:
                return HttpResponse('You are not an admin.')
        else:
            alert = True
            return render(request, 'library/admin_login.html', {'alert':alert})
    return render(request, 'library/admin_login.html')

def Logout(request):
    logout(request)
    return redirect ('/')