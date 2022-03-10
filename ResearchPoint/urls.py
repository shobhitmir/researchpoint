from django.contrib import admin


from django.urls import path
from recommender.views import home_view,login_view,register_view,dashboard_view,profile_view,upload_view,history_view
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name = 'home'),
    path('auth/login/',login_view, name='auth_login'),
    path('auth/signup/',register_view, name='auth_signup'),
    path('dashboard/',dashboard_view, name = 'dashboard'),
    path('profile/',profile_view, name = 'profile'),
    path('upload/',upload_view, name = 'upload'),
    path('history/',history_view, name = 'history'),
]

urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)