from django.contrib import admin
from .models import User,Upvote,Paper
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    pass

@admin.register(Upvote)
class UpvoteAdmin(ImportExportModelAdmin):
    pass

@admin.register(Paper)
class PaperAdmin(ImportExportModelAdmin):
    pass
