from django.contrib import admin
from django.urls import path
from Audio import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import Index,LibraryView

urlpatterns = [
    path('Index', Index.as_view(), name='Index'),   
    path('logout/', views.logout_view, name='logout'),   
    path('Library', LibraryView.as_view(), name='Library'),    
    path('search/', views.search_books_by_tag, name='search_books_by_tag'),
    path('categories', views.category_list, name='category_list'),
    path('tag/<str:tag>/', views.tag_books, name='tag_books'),
    path('tags/<int:category_id>/', views.tags, name='tags'),
    path('',views.Home,name='Home'),
    path('Browse',views.Browse,name='Browse'),
    path('Home',views.Home,name='Home'),
    path('login',auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('signup',views.signup,name='signup'),
    path('tag/<str:tag>/', views.tag_books, name='tag_books'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
