from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    interests = models.TextField(null=True,blank=True)

class Paper(models.Model):
    paper_title = models.CharField(max_length = 100,null=False,blank=False)
    paper_abstract = models.TextField(null=True,blank=True)

class Upvote(models.Model):
    user = models.OneToOneField(User,
    on_delete=models.CASCADE, null=True, blank=True)
    paper = models.OneToOneField(Paper,
    on_delete=models.CASCADE, null=True, blank=True)
    