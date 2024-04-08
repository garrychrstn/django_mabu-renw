from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'theapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('join', views.login_request, name='join'),
    path('profile', views.profile, name='user_profile'),
    path('library', views.library, name='user_library'),
    path('library/update/<int:id>', views.view_book_update, name='view_book'),
    path('series/<int:id>', views.view_book, name='view_book'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
