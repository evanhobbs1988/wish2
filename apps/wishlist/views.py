from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  *
import bcrypt, datetime
# Create your views here.
def index(request):
    return render(request, 'wishlist/index.html')

def register(request):
    errors = User.objects.register_validation(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/')
    else:
        new_user = User.objects.create(
            name = request.POST['name'],
            username = request.POST['username'],
            password = bcrypt.hashpw(request.POST['confirm_pw'].encode(), bcrypt.gensalt()),
            date_hired = datetime.datetime.strptime(request.POST['date_hired'], "%Y-%m-%d").date()

        )
        request.session['username'] = request.POST['username']
        request.session['welcome_name'] = request.POST['name']
        return redirect('/dashboard')

def login(request):
    if User.objects.filter(username=request.POST['username']):
        user = User.objects.get(username=request.POST['username'])
        request.session['username'] = request.POST['username']
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['welcome_name'] = user.name
            return redirect('/dashboard')

    messages.error(request, "Username and password do not match")
    return redirect('/')

def dashboard(request):
    if 'username' not in request.session or 'welcome_name' not in request.session:
        return redirect('/')
    else:
        context = {
            "this_user" : User.objects.get(username=request.session['username']),
            "this_user_items" : Item.objects.filter(liked_by=User.objects.get(username=request.session['username'])),
            "not_liked_items" : Item.objects.exclude(liked_by=User.objects.get(username=request.session['username']))
        }
        return render(request, 'wishlist/dashboard.html', context)

def create(request):
    if 'username' not in request.session or 'welcome_name' not in request.session:
        return redirect('/')
    context = {
            "this_user" : User.objects.get(username=request.session['username']),
        }
    return render(request, 'wishlist/new_item.html', context)

def new_item(request):
    errors = Item.objects.item_validation(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/create')
    else:
        new_item = Item.objects.create(
            item_name = request.POST['item_name'],
            added_by = User.objects.get(id=request.POST['adder']),
        )
        new_item.liked_by.add(User.objects.get(id=request.POST['adder']))
        new_item.save()
        return redirect('/dashboard')

def lists(request, id):
    if 'username' not in request.session or 'welcome_name' not in request.session:
        return redirect('/')
    item = Item.objects.get(id=id)
    context = {
        "this_item" : Item.objects.get(id=id),
        "added_by" : item.liked_by.all()
    }
    return render(request, 'wishlist/lists.html', context)
def add(request,id):
    add_item = Item.objects.get(id=id)
    add_item.liked_by.add(User.objects.get(username=request.session['username']))
    add_item.save()
    return redirect('/dashboard')

def remove(request,id):
    remove_item = Item.objects.get(id=id)
    remove_item.liked_by.remove(User.objects.get(username=request.session['username']))
    remove_item.save()
    return redirect('/dashboard')

def destroy(request,id):
    destroy_item = Item.objects.get(id=id)
    destroy_item.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

