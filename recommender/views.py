from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import redirect
import json

# Create your views here.


def home_view(request):
    return render(request,'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('pwd')
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request,user)
            return render(request,'dashboard.html')
        else:
            messages.error(request,"Invalid username or password.")
            return redirect(request.META['HTTP_REFERER'])


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        interests = request.POST.get('interest')
        interests = interests.split(',')
        interests_dict = {}
        for i in range(len(interests)):
            interests_dict[i] = interests[i]
        pwd = request.POST.get('pwd')
        confirmpwd = request.POST.get('confirmpwd')
        name = name.split(' ')
        fname = name[0]
        if len(name)>1:
            lname = name[1]
        else:
            lname = ''
        if pwd == confirmpwd:
            user = User.objects.create()
            user.first_name = fname
            user.last_name = lname
            user.password = make_password(pwd)
            user.email = email
            user.username = email
            user.interests = json.dumps(interests_dict)
            user.save()
            return render(request,'index.html')
        else:
            messages.error(request,"Passwords do not match.")
            return redirect(request.META['HTTP_REFERER'])