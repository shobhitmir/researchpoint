from django.contrib import admin
from .models import User,Upvote,Paper
# Register your models here.

admin.site.register(User)
admin.site.register(Upvote)
admin.site.register(Paper)