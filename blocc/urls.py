from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('/',views.index,name='Index'),
    path('notifications',views.notification, name='notifications'),
    path('blog',views.blog, name='blog'),
    path('health',views.health, name='health'),
    path('authorities',views.authorities, name='authorities'),
    path('businesses',views.businesses, name='businesses'),
    re_path('view/blog/(\d+)',views.view_blog,name='view_blog'),
    path('my-profile/',views.my_profile, name='my-profile'),
    re_path('user/(?P<username>\w{0,50})',views.user_profile,name='user-profile'),
    path('new/blogpost',views.new_blogpost, name='new-blogpost'),
    path('new/business',views.new_business, name='new-business'),
    path('create/profile',views.create_profile, name='create-profile'),
    path('new/notification',views.new_notification, name='new-notification'),
    path('update/profile',views.update_profile, name='update-profile'),
    path('search/',views.search_results, name='search_results'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)