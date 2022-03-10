from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import nltk
import gensim
import os
from ResearchPoint.settings import BASE_DIR
import pandas as pd
from django.db.models import UniqueConstraint

# Create your models here.


class User(AbstractUser):
    interests = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to ='upload/')
    def _str_(self):
	    return f'{self.user} {self.id}'

class Paper(models.Model):
    Title = models.CharField(max_length = 100,null=False,blank=False)
    Year = models.TextField(null=True,blank=True)
    categories = models.CharField(max_length=100,blank=True,null=True)
    abstracts = models.TextField(null=True,blank=True)
    cleaned_text = models.TextField(null=True,blank=True)
    likes = models.BigIntegerField(default=0)

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='company')
    paper = models.OneToOneField(Paper,on_delete=models.SET_NULL,null=True,related_name='paper')


class Word2Vec:

    def __init__(self):
        model_path = os.path.join(BASE_DIR,'recommender','trained_model','word2vec.model')
        dataset_path = os.path.join(BASE_DIR,'dataset','dataset.csv')
        self.model = gensim.models.Word2Vec.load(model_path)
        self.dataset = pd.read_csv(dataset_path)
    
    def predict(self,input):
        result = self.dataset
        result['Score'] = 0

        for word in input:
            try:
                similar_words = self.model.wv.most_similar(word)[:2]
                for similar in similar_words:
                    similar_word = similar[0]
                    similar_score = similar[1]
                    indices = result[result["abstracts"].str.contains(similar_word, case=False, na=False)].index
                    result['Score'][indices] = result['Score'][indices] + similar_score
            except:
                pass
        
        return result.sort_values(by=['Score'], ascending = False).head(10)
    