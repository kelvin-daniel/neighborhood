from . import views
from django.urls import path, include, re_path
from django.contrib.auth import views as authViews 
from django.conf import settings
from django.conf.urls.static import static
from .views import Signup

urlpatterns=[
    path('',views.index,name='Index'),
    path('accounts/register/', Signup, name='signup'),
    path('accounts/login/', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
    path('notifications',views.notification, name='notifications'),
    path('blog',views.blog, name='blog'),
    re_path('view/blog/(\d+)',views.view_blog,name='view_blog'),
    path('my-profile/',views.my_profile, name='my-profile'),
    path('create/profile',views.create_profile, name='create-profile'),
    path('search/',views.search_results, name='search_results'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)