from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .names import Book

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.contrib.auth import login,logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def inedx(request):

    return render(request,'main/index.html')

def about(request):
    return render(request,'main/about.html')

# def login(request):
#     return render(request,'main/login.html')

def pass_data(request):
    books=[
        Book("Book1","static/main/img/book-8.png"),
        Book("Book2","static/main/img/book-8.png"),
        Book("Book3","static/main/img/book-8.png"),
        Book("Book4", "static/main/img/book-8.png"),

    ]
    return render(request, "main/passhtml.html", {"books":books})

#-------------------------------------------

def home(request):
    return render(request, 'main/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, './main/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                    return render(request, './main/signupuser.html', {'form': UserCreationForm()},'`error','this acc - ')
        else:
            return render(request, './main/signupuser.html', {'form': UserCreationForm()}, 'error', 'this acc no ')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'main/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodo')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'main/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'main/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})


@login_required
def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'./main/currenttodo.html',{'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'main/completedtodos.html', {'todos':todos})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)# тауып береди кай класска жататынын
        return render(request, 'main/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'main/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodo')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')


