from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# def receip_view(request):
#     if request.method == "POST":
#         return create_item_logic(request)
#     queryset = Receipe.objects.all()
#     if request.GET.get('search'):
#         queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
#     context = {'queryset':queryset }
#     return render(request, 'receipe/receipe.html', context)

def receip_view(request):
    if request.method == "POST":
        return create_item_logic(request)

    # Filter recipes uploaded by the currently logged-in user
    queryset_user = Receipe.objects.filter(user=request.user) if request.user.is_authenticated else []


    # Get all recipes
    queryset_all = Receipe.objects.all()

    if request.GET.get('search'):
        queryset_all = queryset_all.filter(receipe_name__icontains=request.GET.get('search'))

    context = {'queryset_user': queryset_user, 'queryset_all': queryset_all}
    return render(request, 'receipe/receipe.html', context)


@login_required(login_url='/login')
def create_item_logic(request):
    data = request.POST
    receipe_name = data.get('receipe_name')
    receipe_description = data.get('receipe_description')
    receipe_image = request.FILES.get('receipe_image')

    Receipe.objects.create(user=request.user, receipe_name=receipe_name, receipe_description=receipe_description, receipe_image=receipe_image)
    return redirect('/')


@login_required(login_url='/login')
def delete_item(request, id):
    recipe = get_object_or_404(Receipe, id=id)
    if request.method in ["POST", "GET"]:
        recipe.delete()
    return redirect('/')



@login_required(login_url='/login')
def update_item(request, id):
    queryset = Receipe.objects.get(id=id)
    if request.method == "POST":
        return update_logic(request, queryset)
    context = {'queryset':queryset }
    return render(request, 'receipe/update_receipe.html', context)

@login_required(login_url='/login')
def update_logic(request, queryset):
    data = request.POST
    receipe_name = data.get('receipe_name')
    receipe_description = data.get('receipe_description')
    receipe_image = request.FILES.get('receipe_image')


    queryset.receipe_name = receipe_name
    queryset.receipe_description = receipe_description
    if receipe_image:
        queryset.receipe_image = receipe_image
    queryset.save()
    return redirect('/')

def login_logic(request):
    form_data = request.POST.copy() if request.method == 'POST' else None
    
    if request.method == "POST":
        username = form_data.get('username')
        password = form_data.get('password')

        existing_user = User.objects.filter(username=username)
        if not existing_user.exists():
            messages.error(request, "Username invalid")
            return render(request, 'receipe/login.html')
        user = authenticate(username = username, password=password)

        if user is None:
            messages.error(request, "Password invalid")
            return render(request, 'receipe/login.html')
        else:
            login(request, user)
            return redirect('/') 


    return render(request, 'receipe/login.html')

def log_out(request):
    logout(request)
    return redirect('/')

def signup(request):
    form_data = request.POST.copy() if request.method == 'POST' else None

    if request.method == "POST":
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        username = form_data.get('username')
        password = form_data.get('password')

        existing_user = User.objects.filter(username=username)
        if existing_user.exists():
            messages.error(request, "User already exists.")
            return render(request, 'receipe/registration.html', {'form_data': form_data})

        User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)

        messages.success(request, "User created successfully.")
        return redirect('/login')

    return render(request, 'receipe/registration.html', {'form_data': form_data})

def delete_account(request, username):
    if user := User.objects.filter(username=username).first():
        # Delete the user
        user.delete()
        messages.success(request, f"Account for {username} has been deleted successfully.")
    else:
        messages.error(request, f"User with username {username} does not exist.")
    return redirect('/')

def account_deletion(request):
    return render(request, "receipe/delete_account.html")