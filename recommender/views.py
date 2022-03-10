from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
import PyPDF2
from ResearchPoint.settings import BASE_DIR
from .models import User,Upvote, Paper
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import redirect
import json
import nltk
import gensim
import os
from recommender.models import Word2Vec
w2v_model = Word2Vec()
from http.client import HTTPResponse
from django.shortcuts import render
import re
import textract
import pdf
import requests
import pandas as pd 
import json
from sklearn.metrics.pairwise import sigmoid_kernel , cosine_similarity
import pickle
import pandas as pd
from gensim import corpora,models
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

import nltk
import gensim
import os
from recommender.models import Word2Vec
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
    if request.POST.get('search'):
        text = request.POST.get('search')
        text = text.lower()
        input = text.split(' ')
        result = w2v_model.predict(input)
        output = []
        for index, row in result.iterrows():
            output.append([row['Title'],row['Year'],row['categories'],row['abstracts'],index])
        return render(request,'dashboard.html',context={'output':output})


    if request.POST.get('like'):
        id = request.POST.get('like')
        user = request.user 
        paper = Paper.objects.get(id=id)
        upvote = Upvote.objects.create()
        print(user,paper.id,'hiiiii')
        upvote.user = user
        upvote.paper = paper
        upvote.save()
    interests = json.loads(request.user.interests)
    input = []
    for key,value in interests.items():
        input.append(value.lower())
    result = w2v_model.predict(input)
    output = []
    for index, row in result.iterrows():
        output.append([row['Title'],row['Year'],row['categories'],row['abstracts'],index])
    return render(request,'dashboard.html',context={'output':output})

def profile_view(request):
    interests = json.loads(request.user.interests)
    return render(request,'profile.html',context={'interests':interests})

df = pd.read_csv('paper_recommendation_final.csv')
dict_ = gensim.corpora.dictionary.Dictionary.load("dict_.dict")
lda_model =  models.LdaModel.load('lda.model')

def upload_view(request):
    data = "none"
    data1=[]
    if request.method == "POST" : 
        files = request.FILES['upload']
        user = request.user
        print(str(files))
        user.file = files
        user.save()
        # get_text = pdf.extraction(os.path.join(BASE_DIR,'media',str(user.file)))
        get_text = pdf_to_text(str(user.file))
        ans = get_recomm(get_text)
        for i in ans:
            row = df[df['Title']==i]
            data1.append([row['Title'],row['Year'],row['category_gen'],row['abstracts']])
        data = data1
        print(ans)
    context = {"data" : data}
    return render(request,'upload.html',context)

def history_view(request):
    upvote = Upvote.objects.filter(user = request.user)
    papers = []
    for obj in upvote:
        papers.append(Paper.objects.get(id = obj.paper.id))
    print(papers)
    return render(request,'history.html',{'papers':papers})

def pdf_to_text(pdf):
    fileobj = open('media/'+pdf, 'rb') 
    reader = PyPDF2.PdfFileReader(fileobj) 
    page = reader.getPage(0) 
    text = page.extractText()

    text = re.split('\s{4,}',text)
    text = str(text)

    text = re.sub(r'\[[0-9]*\]',' ',text)
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'\\n',' ',text)
    text = re.sub(r'\\',' ',text)
    text = re.sub(r'\\x',' ',text)
    text = re.sub(r'\d',' ',text)
    text = re.sub(r'\s+',' ',text)
    text = text.split(' ')
    for i in range(len(text)):
        text[i] = text[i].lower()

    print(text)
    start = text.index("abstract")
    end = text.index("introduction")
    text = text[start+1:end+1]
    abstract = ' '.join(map(str,text))
    print(abstract)
    input = abstract
    return input

def get_recomm(text):
    
    corpus = [text.split()]
    doc_term_matrix = [dict_.doc2bow(i) for i in corpus]
    top_topics = lda_model.get_document_topics(doc_term_matrix, minimum_probability=0.6)
    for i in top_topics:
            
        max=-1
        topic=1
        for topic_no , predict in i:
            if predict>max:
                max=predict
                topic=topic_no

    tfidf = TfidfVectorizer(ngram_range = (1,3))
    ndf = df[df.class_labels == topic]
    corpus = list(ndf.cleaned_text)
    titles  = list(ndf.Title)
    #corpus.append(data)
    vec = tfidf.fit_transform(corpus)
    cosine_similarities = cosine_similarity(vec)
    similar = cosine_similarities[-1]
    values= []
    for n,i in enumerate(similar):
        values.append((n,i))
  #values= list(enumerate(similar))
    scores = sorted(values,key = lambda x : x[1],reverse=True)
    scores = scores[1:11]
    idxs = [i[0] for i in scores]
    ans = []
    for i in idxs:
        ans.append(titles[i])
    
    return ans
