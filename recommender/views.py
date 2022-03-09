from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import redirect
import json
import re
import textract
import nltk
import gensim
import os
from recommender.models import Word2Vec
w2v_model = Word2Vec()
from django.core.paginator import Paginator

# Create your views here.


def home_view(request):
    if request.user is not None:
        logout(request)
    return render(request,'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('pwd')
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request,user)
            return render(request,'upload.html')
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


def dashboard_view(request):
    interests = json.loads(request.user.interests)
    input = []
    for key,value in interests.items():
        input.append(value.lower())
    result = w2v_model.predict(input)
    output = []
    for index, row in result.iterrows():
        output.append([row['Title'],row['Year'],row['categories'],row['abstracts']])
    return render(request,'dashboard.html',context={'output':output})

def profile_view(request):
    interests = json.loads(request.user.interests)
    return render(request,'profile.html',context={'interests':interests})

def upload_view(request):
    return render(request,'upload.html')

def history_view(request):
    return render(request,'history.html')

def pdf_to_text(pdf):
    text = str(textract.process('input.pdf'))
    text = re.split('\s{4,}',text)
    text = str(text)

    text = re.sub(r'\[[0-9]*\]',' ',text)
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'\\n','',text)
    text = re.sub(r'\\',' ',text)
    text = re.sub(r'\\x',' ',text)
    text = re.sub(r'\d',' ',text)
    text = re.sub(r'\s+',' ',text)
    text = text.split(' ')
    for i in range(len(text)):
        text[i] = text[i].lower()

    start = text.index("abstract")
    end = text.index("introduction")
    text = text[start+1:end+1]
    abstract = ' '.join(map(str,text))
    input = abstract.split(' ')
    return input
